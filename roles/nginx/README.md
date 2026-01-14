# nginx

Role to configure nginx.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [nginx_logrotate\_\_dependent_config](#nginx_logrotate__dependent_config)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### nginx_logrotate\_\_dependent_config

#### Default value

```YAML
nginx_logrotate__dependent_config:
  - filename: nginx
    logs:
      - /var/log/nginx/*.log
    options: |
      monthly
      rotate 24
      compress
      delaycompress
      missingok
      notifempty
      sharedscripts
    prerotate: |
      if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
              run-parts /etc/logrotate.d/httpd-prerotate; \
      fi \
    postrotate: |
      invoke-rc.d nginx rotate >/dev/null 2>&1
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
