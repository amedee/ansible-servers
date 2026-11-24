# etckeeper

Track /etc changes with etckeeper.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [etckeeper__default_gitignore](#etckeeper__default_gitignore)
  - [etckeeper__gitignore](#etckeeper__gitignore)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.21`

## Default Variables

### etckeeper__default_gitignore

#### Default value

```YAML
etckeeper__default_gitignore:
  - tor/keys/
  - ssh/ssh_host_*_key
  - keys/mandos/seckey.txt
  - borgmatic/*passphrase*
  - borgmatic.d/*passphrase*
  - X11/xorg.conf.backup
  - apparmor.d/libvirt/*.files
  - zfs/zpool.cache
  - gitlab/gitlab-secrets.json
  - gitlab-runner/config.toml
  - docker/key.json
```

### etckeeper__gitignore

#### Default value

```YAML
etckeeper__gitignore: []
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
