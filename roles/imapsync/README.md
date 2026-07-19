# imapsync

Role to configure imapsync. See the upstream installation instructions:
[imapsync Ubuntu installation instructions](https://imapsync.lamiral.info/INSTALL.d/INSTALL.Ubuntu.txt)

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [imapsync_creds_path](#imapsync_creds_path)
  - [imapsync_install_path](#imapsync_install_path)
  - [imapsync_log_file](#imapsync_log_file)
  - [imapsync_packages](#imapsync_packages)
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

### imapsync_packages

#### Default value

```YAML
imapsync_packages:
  - cpanminus
  - libauthen-ntlm-perl
  - libclass-load-perl
  - libcrypt-openssl-rsa-perl
  - libcrypt-ssleay-perl
  - libdata-uniqid-perl
  - libdigest-hmac-perl
  - libdist-checkconflicts-perl
  - libencode-imaputf7-perl
  - libfile-copy-recursive-perl
  - libfile-tail-perl
  - libio-compress-perl
  - libio-socket-inet6-perl
  - libio-socket-ssl-perl
  - libio-tee-perl
  - libjson-webtoken-perl
  - libmail-imapclient-perl
  - libmodule-scandeps-perl
  - libnet-dbus-perl
  - libnet-dns-perl
  - libnet-ssleay-perl
  - libpar-packer-perl
  - libproc-processtable-perl
  - libreadonly-perl
  - libregexp-common-perl
  - libsys-meminfo-perl
  - libterm-readkey-perl
  - libtest-deep-perl
  - libtest-fatal-perl
  - libtest-mock-guard-perl
  - libtest-mockobject-perl
  - libtest-nowarnings-perl
  - libtest-pod-perl
  - libtest-requires-perl
  - libtest-simple-perl
  - libtest-warn-perl
  - libunicode-string-perl
  - liburi-perl
  - make
  - time
  - wget
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
