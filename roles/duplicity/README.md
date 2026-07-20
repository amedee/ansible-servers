# duplicity

Role to do configuration of duplicity backup of mailinabox.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [duplicity_backup_age](#duplicity_backup_age)
  - [duplicity_backup_target](#duplicity_backup_target)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### duplicity_backup_age

#### Default value

```YAML
duplicity_backup_age: 3
```

### duplicity_backup_target

#### Default value

```YAML
duplicity_backup_target: s3://s3.us-east-1.amazonaws.com/backups-by-amedee/mail-in-a-box
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
