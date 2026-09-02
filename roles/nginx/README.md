# nginx

Role to configure nginx.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [nginx_apt_pinning_files](#nginx_apt_pinning_files)
  - [nginx_apt_suite](#nginx_apt_suite)
  - [nginx_config_files](#nginx_config_files)
  - [nginx_default_indexfiles](#nginx_default_indexfiles)
  - [nginx_directory](#nginx_directory)
  - [nginx_hostname](#nginx_hostname)
  - [nginx_php_version](#nginx_php_version)
  - [nginx_repositories](#nginx_repositories)
  - [nginx_user](#nginx_user)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### nginx_apt_pinning_files

#### Default value

```YAML
nginx_apt_pinning_files:
  - pin_nginx.pref
  - pin_php.pref
```

### nginx_apt_suite

#### Default value

```YAML
nginx_apt_suite: '{{ ansible_distribution_release }}'
```

### nginx_config_files

#### Default value

```YAML
nginx_config_files:
  - src: nginx.conf
    dest: /etc/nginx/nginx.conf
  - src: gzip.conf
    dest: /etc/nginx/conf.d/gzip.conf
```

### nginx_default_indexfiles

#### Default value

```YAML
nginx_default_indexfiles:
  - index.php
  - index.html
```

### nginx_directory

#### Default value

```YAML
nginx_directory: "{{ webserver_directory | default('/var/www/html') }}"
```

### nginx_hostname

#### Default value

```YAML
nginx_hostname: "{{ hostname | default('localhost') }}"
```

### nginx_php_version

#### Default value

```YAML
nginx_php_version: "{{ php_version | default('8.4') }}"
```

### nginx_repositories

#### Default value

```YAML
nginx_repositories:
  - name: nginx
    uri: https://nginx.org/packages/ubuntu
    component: nginx
    key: https://nginx.org/keys/nginx_signing.key
  - name: sury-php
    uri: https://packages.sury.org/php/
    component: main
    key: https://packages.sury.org/php/apt.gpg
```

### nginx_user

#### Default value

```YAML
nginx_user: "{{ webserver_user | default('www-data') }}"
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
