# redis

Role to configure Redis.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [redis_settings](#redis_settings)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### redis_settings

#### Default value

```YAML
redis_settings:
  - regexp: '^(# )?supervised '
    line: supervised systemd
  - regexp: ^requirepass
    line: '# requirepass removed for local-only access'
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
