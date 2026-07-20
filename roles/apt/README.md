# apt

Role to configure APT package management.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [apt_packages_uninstall](#apt_packages_uninstall)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### apt_packages_uninstall

#### Default value

```YAML
apt_packages_uninstall:
  - apport
  - mecab-utils
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
