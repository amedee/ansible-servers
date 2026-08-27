# wp

Configure a WordPress installation with MySQL, Redis, plugins, themes and backup
restoration.

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

This role is intended for Ubuntu hosts running WordPress and assumes the
following components are available or managed elsewhere:

### Operating System

- Ubuntu 24.04 (Noble Numbat)

### Services

- A web server (Apache or Nginx) is installed and configured
- MariaDB or MySQL server running locally and accessible through:
  `/run/mysqld/mysqld.sock`
- PHP installed and configured
- Redis server available for WordPress object caching
- AWS S3 bucket containing optional database and uploads backups

### Ansible Collections

The following collections are required:

```yaml
collections:
  - ansible.mysql
  - amazon.aws
```

- Minimum Ansible version: `2.15`

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
  - php-redis
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
