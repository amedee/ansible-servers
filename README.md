# ansible-servers

Infrastructure-as-Code for my personal production servers, fully managed with Ansible.

This repository contains Ansible playbooks used to provision and maintain
self‑hosted services that I run in production, with a focus on reproducibility,
automation, and secure defaults.

## ✨ Managed systems

- **[amedee.be]**
  Personal technical blog, deployed on a DigitalOcean LEMP stack
  (based on DigitalOcean’s [1‑Click LEMP Droplet][lemp droplet], extended and hardened)

- **[box.vangasse.eu]**
  Mail server (Postfix, Dovecot, etc.) running on Ubuntu 22.04 LTS
  Bootstrapped using [Mail‑in‑a‑Box][mailinabox],
  with additional configuration and automation

## 🛠 Design goals

- Idempotent and repeatable server configuration
- Minimal manual intervention after provisioning
- Clear separation between roles and responsibilities
- Automation over ad‑hoc fixes
- Preference for maintainability over cleverness

## 🚀 Deployment

```shell
ansible-playbook playbooks/site.yml
```

## ✅ Continuous Integration & Code Quality

This repository uses CI to continuously validate configuration quality:

[![Deployment Status][deployment-badge]][deployment-status]
[![Codacy Badge][codacy-badge]][codacy-grade]
[![Super-Linter][superlinter-badge]][superlinter-status]
[![CodeFactor][codefactor-badge]][codefactor-status]
[![License: MIT][license-badge]][license-link]

## 🔍 Repository History

Timelapse visualisation of how this infrastructure codebase evolved over time.

[![Gource thumbnail][gource-thumbnail]][gource-video]

## References

- The Postfix [checks files][checks files] are retrieved from the
  [Web Archive of securitysage.com][securitysage].
  Last retrieval date: 6 January 2007.

[amedee.be]: https://amedee.be
[box.vangasse.eu]: https://box.vangasse.eu
[lemp droplet]: https://do.co/2GOFe5J#start
[mailinabox]: https://mailinabox.email/
[deployment-badge]: https://github.com/amedee/ansible-servers/actions/workflows/pipeline.yml/badge.svg
[deployment-status]: https://github.com/amedee/ansible-servers/actions/workflows/pipeline.yml
[codacy-badge]: https://app.codacy.com/project/badge/Grade/14aefeb38e4e4313a524d732264dc9fc
[codacy-grade]: https://app.codacy.com/gh/amedee/ansible-servers/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade
[superlinter-badge]: https://github.com/amedee/ansible-servers/actions/workflows/code-quality-super-linter.yml/badge.svg
[superlinter-status]: https://github.com/marketplace/actions/code-quality-super-linter
[codefactor-badge]: https://www.codefactor.io/repository/github/amedee/ansible-servers/badge
[codefactor-status]: https://www.codefactor.io/repository/github/amedee/ansible-servers
[license-badge]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-link]: https://opensource.org/licenses/MIT
[checks files]: roles/mailserver/files/etc/postfix/checks
[securitysage]: https://web.archive.org/web/20070106001401/http://www.securitysage.com:80/guides/postfix_uce.html
[gource-thumbnail]: https://gource-by-amedee.s3.amazonaws.com/gource-latest.gif
[gource-video]: https://gource-by-amedee.s3.amazonaws.com/gource-latest.mp4
