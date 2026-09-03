# wp

Configure a WordPress installation with MySQL, Redis, plugins, themes and backup
restoration.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [wp_admin_email](#wp_admin_email)
  - [wp_admin_password](#wp_admin_password)
  - [wp_admin_user](#wp_admin_user)
  - [wp_archive](#wp_archive)
  - [wp_archive_dir](#wp_archive_dir)
  - [wp_cli](#wp_cli)
  - [wp_cli_bin](#wp_cli_bin)
  - [wp_constants](#wp_constants)
  - [wp_database_constants](#wp_database_constants)
  - [wp_db_host](#wp_db_host)
  - [wp_db_name](#wp_db_name)
  - [wp_db_password](#wp_db_password)
  - [wp_db_user](#wp_db_user)
  - [wp_fallback_theme](#wp_fallback_theme)
  - [wp_packages](#wp_packages)
  - [wp_php_bin](#wp_php_bin)
  - [wp_php_packages](#wp_php_packages)
  - [wp_plugins](#wp_plugins)
  - [wp_plugins_uninstall](#wp_plugins_uninstall)
  - [wp_python_packages](#wp_python_packages)
  - [wp_site_title](#wp_site_title)
  - [wp_site_url](#wp_site_url)
  - [wp_table_prefix](#wp_table_prefix)
  - [wp_themes](#wp_themes)
  - [wp_themes_uninstall](#wp_themes_uninstall)
  - [wp_webserver_directory](#wp_webserver_directory)
  - [wp_webserver_user](#wp_webserver_user)
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

### wp_admin_email

#### Default value

```YAML
wp_admin_email: admin@example.com
```

### wp_admin_password

#### Default value

```YAML
wp_admin_password: admin-password
```

### wp_admin_user

#### Default value

```YAML
wp_admin_user: admin
```

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

### wp_cli

#### Default value

```YAML
wp_cli:
  - '{{ wp_php_bin }}'
  - '{{ wp_cli_bin }}'
  - --path={{ wp_webserver_directory }}
```

### wp_cli_bin

#### Default value

```YAML
wp_cli_bin: /usr/local/bin/wp
```

### wp_constants

#### Default value

```YAML
wp_constants:
  - name: WP_CACHE_KEY_SALT
    value: localhost
```

### wp_database_constants

#### Default value

```YAML
wp_database_constants:
  DB_NAME: '{{ wp_db_name }}'
  DB_USER: '{{ wp_db_user }}'
  DB_PASSWORD: '{{ wp_db_password }}'
  DB_HOST: '{{ wp_db_host }}'
```

### wp_db_host

#### Default value

```YAML
wp_db_host: localhost
```

### wp_db_name

#### Default value

```YAML
wp_db_name: wordpress
```

### wp_db_password

#### Default value

```YAML
wp_db_password: ''
```

### wp_db_user

#### Default value

```YAML
wp_db_user: wordpress
```

### wp_fallback_theme

#### Default value

```YAML
wp_fallback_theme: neve
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

### wp_php_bin

#### Default value

```YAML
wp_php_bin: /usr/bin/php
```

### wp_php_packages

#### Default value

```YAML
wp_php_packages:
  - php-cli
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

### wp_plugins

#### Default value

```YAML
wp_plugins:
  - redis-cache
  - wp-redis
```

### wp_plugins_uninstall

#### Default value

```YAML
wp_plugins_uninstall:
  - hello
```

### wp_python_packages

#### Default value

```YAML
wp_python_packages:
  - python3-boto3
  - python3-packaging
  - python3-pip
  - python3-pymysql
```

### wp_site_title

#### Default value

```YAML
wp_site_title: WordPress
```

### wp_site_url

#### Default value

```YAML
wp_site_url: http://localhost
```

### wp_table_prefix

#### Default value

```YAML
wp_table_prefix: wp_
```

### wp_themes

#### Default value

```YAML
wp_themes:
  - neve
```

### wp_themes_uninstall

#### Default value

```YAML
wp_themes_uninstall:
  - twentytwentytwo
  - twentytwentythree
  - twentytwentyfour
```

### wp_webserver_directory

#### Default value

```YAML
wp_webserver_directory: "{{ webserver_directory | default('/var/www/html') }}"
```

### wp_webserver_user

#### Default value

```YAML
wp_webserver_user: "{{ webserver_user | default('www-data') }}"
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
