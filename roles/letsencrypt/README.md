# letsencrypt

Role to configure letsencrypt.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [letsencrypt_primary_domain](#letsencrypt_primary_domain)
  - [letsencrypt_restore_from_backup](#letsencrypt_restore_from_backup)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### letsencrypt_primary_domain

#### Default value

```YAML
letsencrypt_primary_domain: amedee.be
```

### letsencrypt_restore_from_backup

#### Default value

```YAML
letsencrypt_restore_from_backup: true
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
