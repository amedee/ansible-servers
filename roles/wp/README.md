# wp

Role to configure my WordPress blog.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [wp_archive](#wp_archive)
  - [wp_archive_dir](#wp_archive_dir)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### wp_archive

#### Default value

```YAML
wp_archive: '{{ wp_archive_dir }}/uploads.tar.xz'
```

### wp_archive_dir

#### Default value

```YAML
wp_archive_dir: /var/cache/wp-archive
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
