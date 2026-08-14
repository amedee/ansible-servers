# php

Install and configure PHP and PHP-FPM.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [php_fpm_socket](#php_fpm_socket)
  - [php_module_packages](#php_module_packages)
  - [php_packages](#php_packages)
  - [php_repository](#php_repository)
  - [php_repository_suite](#php_repository_suite)
  - [php_version](#php_version)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.17`

## Default Variables

### php_fpm_socket

#### Default value

```YAML
php_fpm_socket: /run/php/php-fpm.sock
```

### php_module_packages

#### Default value

```YAML
php_module_packages:
  - php{{ php_version }}-curl
  - php{{ php_version }}-gd
  - php{{ php_version }}-imagick
  - php{{ php_version }}-intl
  - php{{ php_version }}-mbstring
  - php{{ php_version }}-mysql
  - php{{ php_version }}-redis
  - php{{ php_version }}-ssh2
  - php{{ php_version }}-xml
  - php{{ php_version }}-xmlrpc
  - php{{ php_version }}-zip
```

### php_packages

#### Default value

```YAML
php_packages:
  - php{{ php_version }}-cli
  - php{{ php_version }}-fpm
```

### php_repository

#### Default value

```YAML
php_repository:
  name: sury-php
  uri: https://packages.sury.org/php/
  component: main
  key: https://packages.sury.org/php/apt.gpg
```

### php_repository_suite

#### Default value

```YAML
php_repository_suite: "{{ ansible_distribution_release | default('noble') }}"
```

### php_version

#### Default value

```YAML
php_version: '8.5'
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
