# postfix

Role to configure Postfix.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [postfix_invalid_recipients](#postfix_invalid_recipients)
  - [postfix_mailserver](#postfix_mailserver)
  - [postfix_ses_enabled](#postfix_ses_enabled)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### postfix_invalid_recipients

#### Default value

```YAML
postfix_invalid_recipients: []
```

### postfix_mailserver

#### Default value

```YAML
postfix_mailserver: false
```

### postfix_ses_enabled

#### Default value

```YAML
postfix_ses_enabled: false
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
