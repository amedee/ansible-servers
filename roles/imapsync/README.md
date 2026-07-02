# imapsync

Role to configure imapsync.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [imapsync_creds_path](#imapsync_creds_path)
  - [imapsync_install_path](#imapsync_install_path)
  - [imapsync_log_file](#imapsync_log_file)
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
