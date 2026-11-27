# keyring

Import configured GPG keys into the root keyring.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [keyring__dependent_gpg_keys](#keyring__dependent_gpg_keys)
  - [keyring__keyserver](#keyring__keyserver)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.21`

## Default Variables

### keyring__dependent_gpg_keys

#### Default value

```YAML
keyring__dependent_gpg_keys: []
```

### keyring__keyserver

#### Default value

```YAML
keyring__keyserver: hkps://keyserver.ubuntu.com
```

## Dependencies

None.

## License

MIT

## Author

[Ameðea Van Gasse](https://amedee.be)
