# etckeeper

Role to configure etckeeper.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [etckeeper\_\_enabled](#etckeeper__enabled)
  - [etckeeper\_\_vcs](#etckeeper__vcs)
  - [etckeeper\_\_vcs_email](#etckeeper__vcs_email)
  - [etckeeper\_\_vcs_user](#etckeeper__vcs_user)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### etckeeper\_\_enabled

#### Default value

```YAML
etckeeper__enabled: true
```

### etckeeper\_\_vcs

#### Default value

```YAML
etckeeper__vcs: git
```

### etckeeper\_\_vcs_email

#### Default value

```YAML
etckeeper__vcs_email: >-
  root@{{ ansible_facts['fqdn']
  | default(ansible_facts['hostname']) }}
```

### etckeeper\_\_vcs_user

#### Default value

```YAML
etckeeper__vcs_user: The /etc Keeper
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
