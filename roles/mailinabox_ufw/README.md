# mailinabox_ufw

Work around Mail-in-a-Box's outbound SMTP connectivity check by redirecting
outbound TCP/25 to localhost. Intended for servers that send mail via an SMTP
relay or API instead of direct SMTP delivery.

## Table of contents

- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
