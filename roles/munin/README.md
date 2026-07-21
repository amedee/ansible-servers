# munin

Installs Munin monitoring server and configures monitored hosts with custom
settings and maintenance fixes.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [munin_removed_hosts](#munin_removed_hosts)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### munin_removed_hosts

#### Default value

```YAML
munin_removed_hosts:
  - box.vangasse.eu
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
