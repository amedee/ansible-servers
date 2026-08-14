# swapfile

Wrapper role for `debops.debops.swapfile` because it doesn't run `swapon --all`.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [swapfile_path](#swapfile_path)
  - [swapfile_size](#swapfile_size)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### swapfile_path

#### Default value

```YAML
swapfile_path: /swapfile
```

### swapfile_size

#### Default value

```YAML
swapfile_size: 2048
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
