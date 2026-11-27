# wpcli

Install and verify the WP-CLI executable.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [wpcli__binary](#wpcli__binary)
  - [wpcli__checksum](#wpcli__checksum)
  - [wpcli__src](#wpcli__src)
  - [wpcli__version](#wpcli__version)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.21`

## Default Variables

### wpcli__binary

#### Default value

```YAML
wpcli__binary: /usr/local/bin/wp
```

### wpcli__checksum

#### Default value

```YAML
wpcli__checksum: sha256:f12126a3ca1c48e53b7f89fd30e60b9cf3335dfb0c94403a2e5c125be0e66c77
```

### wpcli__src

#### Default value

```YAML
wpcli__src: /usr/local/src/wpcli
```

### wpcli__version

#### Default value

```YAML
wpcli__version: 2.12.0
```

## Dependencies

None.

## License

MIT

## Author

[Ameðea Van Gasse](https://amedee.be)
