# imapsync

Role to configure imapsync.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [imapsync_creds_path](#imapsync_creds_path)
  - [imapsync_cron_hour](#imapsync_cron_hour)
  - [imapsync_cron_minute](#imapsync_cron_minute)
  - [imapsync_install_path](#imapsync_install_path)
  - [imapsync_log_file](#imapsync_log_file)
  - [imapsync_logrotate\_\_dependent_config](#imapsync_logrotate__dependent_config)
  - [imapsync_script_path](#imapsync_script_path)
  - [imapsync_upstream_url](#imapsync_upstream_url)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### imapsync_creds_path

#### Default value

```YAML
imapsync_creds_path: /root/.imapsync-creds
```

### imapsync_cron_hour

#### Default value

```YAML
imapsync_cron_hour: '*'
```

### imapsync_cron_minute

#### Default value

```YAML
imapsync_cron_minute: '*/10'
```

### imapsync_install_path

#### Default value

```YAML
imapsync_install_path: /usr/local/bin/imapsync
```

### imapsync_log_file

#### Default value

```YAML
imapsync_log_file: /var/log/imapsync.log
```

### imapsync_logrotate\_\_dependent_config

#### Default value

```YAML
imapsync_logrotate__dependent_config:
  - filename: imapsync
    log: '{{ imapsync_log_file }}'
    options: |
      weekly
      missingok
      rotate 8
      compress
      delaycompress
      notifempty
      create 0640 root adm
    state: present
```

### imapsync_script_path

#### Default value

```YAML
imapsync_script_path: /usr/local/sbin/imapsync.sh
```

### imapsync_upstream_url

#### Default value

```YAML
imapsync_upstream_url: https://imapsync.lamiral.info/imapsync
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
