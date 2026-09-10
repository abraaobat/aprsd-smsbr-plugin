#!/usr/bin/env python3
"""Exercise APRSD's real APRS-IS and TCP KISS drivers against local sockets.

No public APRS-IS server, RF path or real SMS provider is used. This validates
transport setup/login/frame transmission deterministically in CI.
"""

from __future__ import annotations

import queue
import socket
import threading
from contextlib import closing

from aprsd import conf  # noqa: F401 - importing registers APRSD config options
from aprsd.client.drivers.aprsis import APRSISDriver
from aprsd.client.drivers.tcpkiss import TCPKISSDriver
from aprsd.packets import core
from oslo_config import cfg

CONF = cfg.CONF


class LocalServer:
    def __init__(self, handler):
        self.handler = handler
        self.events: queue.Queue[tuple[str, bytes]] = queue.Queue()
        self.error: BaseException | None = None
        self.ready = threading.Event()
        self.port: int | None = None
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> int:
        self._thread.start()
        if not self.ready.wait(timeout=5):
            raise RuntimeError("local test server did not start")
        if self.error:
            raise self.error
        assert self.port is not None
        return self.port

    def join(self) -> None:
        self._thread.join(timeout=5)
        if self._thread.is_alive():
            raise RuntimeError("local test server did not stop")
        if self.error:
            raise self.error

    def _run(self) -> None:
        try:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(("127.0.0.1", 0))
                server.listen(1)
                server.settimeout(5)
                self.port = server.getsockname()[1]
                self.ready.set()
                conn, _ = server.accept()
                with closing(conn):
                    conn.settimeout(5)
                    self.handler(conn, self.events)
        except BaseException as exc:  # propagate failures to main thread
            self.error = exc
            self.ready.set()


def make_message(text: str = "SMSBR transport smoke") -> core.MessagePacket:
    packet = core.MessagePacket(
        from_call="PV8ABC",
        to_call="PV8XYZ",
        message_text=text,
        msgNo="01",
    )
    packet.prepare()
    return packet


def aprsis_handler(conn: socket.socket, events: queue.Queue[tuple[str, bytes]]) -> None:
    conn.sendall(b"# local-aprsis test server\r\n")
    login = conn.recv(1024)
    events.put(("login", login))
    if b"user PV8ABC pass 12345" not in login:
        raise AssertionError(f"unexpected APRS-IS login: {login!r}")

    conn.sendall(b"# logresp PV8ABC verified, server LOCAL-SMSBR\r\n")
    outbound = conn.recv(4096)
    events.put(("packet", outbound))
    if b"PV8ABC>APZ100::PV8XYZ" not in outbound:
        raise AssertionError(f"unexpected APRS-IS packet: {outbound!r}")


def kiss_handler(conn: socket.socket, events: queue.Queue[tuple[str, bytes]]) -> None:
    frame = conn.recv(4096)
    events.put(("frame", frame))
    if len(frame) < 4:
        raise AssertionError(f"KISS frame too short: {frame!r}")
    if frame[0] != 0xC0 or frame[-1] != 0xC0:
        raise AssertionError(f"KISS frame missing FEND boundaries: {frame!r}")
    if frame[1] != 0x00:
        raise AssertionError(
            f"expected KISS data-frame command 0x00, got {frame[1]:#x}"
        )


def validate_aprsis() -> None:
    server = LocalServer(aprsis_handler)
    port = server.start()

    CONF.set_override("callsign", "PV8ABC")
    CONF.set_override("enabled", True, group="aprs_network")
    CONF.set_override("password", "12345", group="aprs_network")
    CONF.set_override("host", "127.0.0.1", group="aprs_network")
    CONF.set_override("port", port, group="aprs_network")

    driver = APRSISDriver()
    driver.close()
    driver.setup_connection()
    if not driver.connected or not driver.login_success():
        raise AssertionError(f"APRS-IS local login failed: {driver.login_failure()}")
    if driver.server_string != "LOCAL-SMSBR":
        raise AssertionError(
            f"unexpected APRS-IS server string: {driver.server_string!r}"
        )

    driver.send(make_message())
    driver.close()
    server.join()

    labels = {label for label, _ in list(server.events.queue)}
    if labels != {"login", "packet"}:
        raise AssertionError(f"missing APRS-IS smoke events: {labels}")


def validate_tcpkiss() -> None:
    server = LocalServer(kiss_handler)
    port = server.start()

    CONF.set_override("enabled", True, group="kiss_tcp")
    CONF.set_override("host", "127.0.0.1", group="kiss_tcp")
    CONF.set_override("port", port, group="kiss_tcp")
    CONF.set_override("path", ["WIDE1-1"], group="kiss_tcp")

    driver = TCPKISSDriver()
    driver.close()
    driver.setup_connection()
    if not driver._connected:
        raise AssertionError("TCP KISS local connection failed")

    driver.send(make_message("SMSBR KISS smoke"))
    driver.close()
    server.join()

    label, frame = server.events.get_nowait()
    if label != "frame" or not frame:
        raise AssertionError("TCP KISS server did not receive a frame")


def main() -> int:
    validate_aprsis()
    validate_tcpkiss()
    print("local APRS-IS and TCP KISS transport smoke: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
