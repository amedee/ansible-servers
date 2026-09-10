# ansible-servers

Infrastructure-as-Code for my personal production servers, fully managed with
Ansible.

This repository contains Ansible playbooks used to provision and maintain
self‑hosted services that I run in production, with a focus on reproducibility,
automation, and secure defaults.

## ✨ Managed systems

- **[amedee.be]** Personal technical blog, deployed on a DigitalOcean LEMP stack
  (based on DigitalOcean’s [1‑Click LEMP Droplet][lemp droplet], extended and
  hardened)

- **[box.vangasse.eu]** Mail server (Postfix, Dovecot, etc.) running on Ubuntu
  22.04 LTS Bootstrapped using [Mail‑in‑a‑Box][mailinabox], with additional
  configuration and automation

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

[![Molecule Coverage][molecule-badge]][molecule-status]

<!-- molecule-coverage:start -->

| Role                                                                                         | Description                                                                                                                                                                                             | Molecule |
| :------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------: |
| [`apt`](https://github.com/amedee/ansible-servers/tree/main/roles/apt)                       | Role to configure APT package management.                                                                                                                                                               |    ✅    |
| [`base_linux`](https://github.com/amedee/ansible-servers/tree/main/roles/base_linux)         | Baseline Linux configuration                                                                                                                                                                            |    ✅    |
| [`dovecot`](https://github.com/amedee/ansible-servers/tree/main/roles/dovecot)               | Dovecot-related maintenance tasks for Mail-in-a-Box, including mailbox expunge jobs and helper scripts scheduled via /etc/cron.d.                                                                       |    ✅    |
| [`duplicity`](https://github.com/amedee/ansible-servers/tree/main/roles/duplicity)           | Role to do configuration of duplicity backup of mailinabox.                                                                                                                                             |    ✅    |
| [`hadori`](https://github.com/amedee/ansible-servers/tree/main/roles/hadori)                 | Role to configure hadori.                                                                                                                                                                               |    ✅    |
| [`imapsync`](https://github.com/amedee/ansible-servers/tree/main/roles/imapsync)             | Role to configure imapsync. See the upstream installation instructions: [imapsync Ubuntu installation instructions](https://imapsync.lamiral.info/INSTALL.d/INSTALL.Ubuntu.txt)                         |    ✅    |
| [`letsencrypt`](https://github.com/amedee/ansible-servers/tree/main/roles/letsencrypt)       | Role to configure letsencrypt.                                                                                                                                                                          |    ✅    |
| [`localepurge`](https://github.com/amedee/ansible-servers/tree/main/roles/localepurge)       | Role to install and configure localepurge.                                                                                                                                                              |    ✅    |
| [`magic`](https://github.com/amedee/ansible-servers/tree/main/roles/magic)                   | Teaches Linux systems the ancient arts of prophecy and bovine communication. Provides the `✨` command for consulting the mysterious forces governing YAML and CI pipelines.                            |    ✅    |
| [`mailinabox_dns`](https://github.com/amedee/ansible-servers/tree/main/roles/mailinabox_dns) | Role to do DNS configuration of mailinabox.                                                                                                                                                             |    ✅    |
| [`mailinabox_ufw`](https://github.com/amedee/ansible-servers/tree/main/roles/mailinabox_ufw) | Work around Mail-in-a-Box's outbound SMTP connectivity check by redirecting outbound TCP/25 to localhost. Intended for servers that send mail via an SMTP relay or API instead of direct SMTP delivery. |    ✅    |
| [`munin`](https://github.com/amedee/ansible-servers/tree/main/roles/munin)                   | Installs Munin monitoring server and configures monitored hosts with custom settings and maintenance fixes.                                                                                             |    ✅    |
| [`munin_node`](https://github.com/amedee/ansible-servers/tree/main/roles/munin_node)         | Role to configure munin-node.                                                                                                                                                                           |    ✅    |
| [`mysql`](https://github.com/amedee/ansible-servers/tree/main/roles/mysql)                   | Role to install and configure a MySQL database server.                                                                                                                                                  |    ✅    |
| [`nginx`](https://github.com/amedee/ansible-servers/tree/main/roles/nginx)                   | Role to configure nginx.                                                                                                                                                                                |    ✅    |
| [`php`](https://github.com/amedee/ansible-servers/tree/main/roles/php)                       | Install and configure PHP and PHP-FPM.                                                                                                                                                                  |    ✅    |
| [`postfix`](https://github.com/amedee/ansible-servers/tree/main/roles/postfix)               | Role to configure Postfix.                                                                                                                                                                              |    ✅    |
| [`postfix_ses`](https://github.com/amedee/ansible-servers/tree/main/roles/postfix_ses)       | Role to configure Amazon SES integration for Postfix.                                                                                                                                                   |    ✅    |
| [`redis`](https://github.com/amedee/ansible-servers/tree/main/roles/redis)                   | Role to configure Redis.                                                                                                                                                                                |    ✅    |
| [`swapfile`](https://github.com/amedee/ansible-servers/tree/main/roles/swapfile)             | Wrapper role for `debops.debops.swapfile` because it doesn't run `swapon --all`.                                                                                                                        |    ✅    |
| [`wp`](https://github.com/amedee/ansible-servers/tree/main/roles/wp)                         | Configure a WordPress installation with MySQL, Redis, plugins, themes and backup restoration.                                                                                                           |    ✅    |

<!-- molecule-coverage:end -->

[![Deployment Status][deployment-badge]][deployment-status]
[![Codacy Badge][codacy-badge]][codacy-grade]
[![Super-Linter][superlinter-badge]][superlinter-status]
[![CodeFactor][codefactor-badge]][codefactor-status]

[![License: MIT][license-badge]][license-link]

## 🔍 Repository History

Timelapse visualisation of how this infrastructure codebase evolved over time.

[![Gource thumbnail][gource-thumbnail]][gource-video]

## References

- The Postfix [checks files][checks files] are retrieved from the [Web Archive
  of securitysage.com][securitysage]. Last retrieval date: 6 January 2007.

[amedee.be]: https://amedee.be
[box.vangasse.eu]: https://box.vangasse.eu
[lemp droplet]: https://do.co/2GOFe5J#start
[mailinabox]: https://mailinabox.email/
[deployment-badge]:
  https://github.com/amedee/ansible-servers/actions/workflows/pipeline.yml/badge.svg
[deployment-status]:
  https://github.com/amedee/ansible-servers/actions/workflows/pipeline.yml
[codacy-badge]:
  https://app.codacy.com/project/badge/Grade/14aefeb38e4e4313a524d732264dc9fc
[codacy-grade]:
  https://app.codacy.com/gh/amedee/ansible-servers/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade
[superlinter-badge]:
  https://github.com/amedee/ansible-servers/actions/workflows/code-quality-super-linter.yml/badge.svg
[superlinter-status]:
  https://github.com/marketplace/actions/code-quality-super-linter
[codefactor-badge]:
  https://www.codefactor.io/repository/github/amedee/ansible-servers/badge
[codefactor-status]:
  https://www.codefactor.io/repository/github/amedee/ansible-servers
[license-badge]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-link]: https://opensource.org/licenses/MIT
[checks files]: roles/postfix/files/checks
[securitysage]:
  https://web.archive.org/web/20070106001401/http://www.securitysage.com:80/guides/postfix_uce.html
[gource-thumbnail]: https://gource-by-amedee.s3.amazonaws.com/gource-latest.gif
[gource-video]: https://gource-by-amedee.s3.amazonaws.com/gource-latest.mp4
[molecule-badge]:
  https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/amedee/ansible-servers/refs/heads/badges/molecule-coverage.json
[molecule-status]:
  https://github.com/amedee/ansible-servers/actions/workflows/molecule-coverage.yml
