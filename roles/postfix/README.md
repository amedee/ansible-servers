# postfix

Role to configure Postfix.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [postfix_inbound](#postfix_inbound)
  - [postfix_invalid_recipients](#postfix_invalid_recipients)
  - [postfix_recipient_domains](#postfix_recipient_domains)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### postfix_inbound

#### Default value

```YAML
postfix_inbound: false
```

### postfix_invalid_recipients

#### Default value

```YAML
postfix_invalid_recipients: []
```

### postfix_recipient_domains

#### Default value

```YAML
postfix_recipient_domains:
  - localhost
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
