# wp

Role to configure my WordPress blog.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [wp_archive](#wp_archive)
  - [wp_archive_dir](#wp_archive_dir)
  - [wp_packages](#wp_packages)
  - [wp_php_packages](#wp_php_packages)
  - [wp_python_packages](#wp_python_packages)
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

### wp_packages

#### Default value

```YAML
wp_packages:
  - curl
  - ghostscript
  - imagemagick
  - mysql-client
```

### wp_php_packages

#### Default value

```YAML
wp_php_packages:
  - php-curl
  - php-gd
  - php-imagick
  - php-intl
  - php-json
  - php-mbstring
  - php-mysql
  - php-ssh2
  - php-xml
  - php-xmlrpc
  - php-zip
```

### wp_python_packages

#### Default value

```YAML
wp_python_packages:
  - python3-boto3
  - python3-mysqldb
  - python3-packaging
  - python3-pip
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
