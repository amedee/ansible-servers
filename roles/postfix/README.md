# postfix

Role to configure Postfix.

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [postfix_static_settings](#postfix_static_settings)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### postfix_static_settings

#### Default value

```YAML
postfix_static_settings:
  alias_database:
  append_dot_mydomain:
  biff:
  body_checks: pcre:/etc/postfix/checks/body_checks.pcre
  bounce_queue_lifetime: 3d
  compatibility_level: '3.6'
  delay_warning_time: '0'
  header_checks: pcre:/etc/postfix/checks/header_checks.pcre
  header_size_limit: '4096000'
  inet_interfaces:
  inet_protocols:
  maximal_queue_lifetime: 30d
  message_size_limit: '52428800'
  mime_header_checks: pcre:/etc/postfix/checks/mime_header_checks.pcre
  myhostname: '{{ hostname }}'
  mynetworks: 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
  myorigin: $myhostname
  readme_directory:
  recipient_canonical_maps: pcre:/etc/postfix/recipient-canonical-maps.pcre
  recipient_delimiter: +-
  relayhost: '[email-smtp.us-east-1.amazonaws.com]:587'
  smtp_bind_address6:
  smtp_sasl_auth_enable: yes
  smtp_sasl_password_maps: hash:/etc/postfix/sasl/sasl_passwd
  smtp_sasl_security_options: noanonymous
  smtp_tls_CAfile: /etc/ssl/certs/ca-certificates.crt
  smtp_tls_ciphers: high
  smtp_tls_note_starttls_offer: yes
  smtp_tls_security_level: encrypt
  smtp_use_tls: yes
  smtpd_banner: $myhostname ESMTP
  smtpd_relay_restrictions:
    permit_mynetworks,permit_sasl_authenticated,reject_unauth_destination
  smtpd_sasl_auth_enable: yes
  smtpd_tls_ciphers:
  smtputf8_enable: yes
  tls_preempt_cipherlist:
  transport_maps:
```

## Dependencies

None.

## License

MIT

## Author

[Amedee Van Gasse](https://amedee.be)
