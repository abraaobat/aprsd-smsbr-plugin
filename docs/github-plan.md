# GitHub Publication Plan

Target repository:

```text
abraaobat/aprsd-smsbr-plugin
```

Recommended settings:

- Visibility: Public
- Default branch: `main`
- License: Apache-2.0
- Issues: enabled
- Discussions: optional after the first field-test release
- Secret scanning / push protection: enable when available

Development workflow:

```text
feature/<phase>-<scope>
  -> tests/docs
  -> conventional commit
  -> push
  -> Pull Request to main
  -> CI/review
  -> merge
```

Initial branch after repository bootstrap:

```text
feature/f0-foundation
```

Initial commit message:

```text
feat(smsbr): bootstrap APRSD gateway foundation
```

Suggested repository description:

> Open-source Brazilian APRS ⇄ SMS gateway for APRSD, DigiPi and Dire Wolf.

Suggested topics:

`aprs`, `aprs-is`, `aprsd`, `digipi`, `direwolf`, `ham-radio`, `sms`, `brazil`, `raspberry-pi`
