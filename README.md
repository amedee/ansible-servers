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

| Role                                                                                                   | Description                                                                                                                                                           | Molecule |
| :----------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------: |
| [`apt`](https://github.com/amedee/ansible-servers/tree/main/roles/apt)                                 | Configure APT repositories and package management.                                                                                                                    |    ✅    |
| [`apt_listchanges`](https://github.com/amedee/ansible-servers/tree/main/roles/apt_listchanges)         | Configure apt-listchanges package notifications.                                                                                                                      |    ✅    |
| [`base_linux`](https://github.com/amedee/ansible-servers/tree/main/roles/base_linux)                   | Configure baseline Linux packages and logging.                                                                                                                        |    ✅    |
| [`dovecot`](https://github.com/amedee/ansible-servers/tree/main/roles/dovecot)                         | Maintain Dovecot mailboxes and scheduled maintenance.                                                                                                                 |    ✅    |
| [`duplicity`](https://github.com/amedee/ansible-servers/tree/main/roles/duplicity)                     | Configure Duplicity mail backups.                                                                                                                                     |    ✅    |
| [`environment`](https://github.com/amedee/ansible-servers/tree/main/roles/environment)                 | Configure system-wide environment variables.                                                                                                                          |    ✅    |
| [`etc_aliases`](https://github.com/amedee/ansible-servers/tree/main/roles/etc_aliases)                 | Configure system mail aliases.                                                                                                                                        |    ✅    |
| [`etckeeper`](https://github.com/amedee/ansible-servers/tree/main/roles/etckeeper)                     | Track system configuration changes with Git.                                                                                                                          |    ✅    |
| [`hadori`](https://github.com/amedee/ansible-servers/tree/main/roles/hadori)                           | Install Hadori and its scheduled job.                                                                                                                                 |    ✅    |
| [`imapsync`](https://github.com/amedee/ansible-servers/tree/main/roles/imapsync)                       | Configure scheduled IMAP mailbox synchronization. Follow the [imapsync Ubuntu installation instructions](https://imapsync.lamiral.info/INSTALL.d/INSTALL.Ubuntu.txt). |    ✅    |
| [`journald`](https://github.com/amedee/ansible-servers/tree/main/roles/journald)                       | Configure systemd journal settings.                                                                                                                                   |    ✅    |
| [`keyring`](https://github.com/amedee/ansible-servers/tree/main/roles/keyring)                         | Import configured GPG keys into the root keyring.                                                                                                                     |    ✅    |
| [`letsencrypt`](https://github.com/amedee/ansible-servers/tree/main/roles/letsencrypt)                 | Install Certbot and restore certificate configuration.                                                                                                                |    ✅    |
| [`localepurge`](https://github.com/amedee/ansible-servers/tree/main/roles/localepurge)                 | Configure locale retention and removal.                                                                                                                               |    ✅    |
| [`magic`](https://github.com/amedee/ansible-servers/tree/main/roles/magic)                             | Invoke the ✨ command to divine mysterious prophecies and ancient fortunes for keepers of YAML and their sacred CI pipelines.                                         |    ✅    |
| [`mailinabox`](https://github.com/amedee/ansible-servers/tree/main/roles/mailinabox)                   | Customize Mail-in-a-Box DNS, firewall, and web settings.                                                                                                              |    ✅    |
| [`munin`](https://github.com/amedee/ansible-servers/tree/main/roles/munin)                             | Install and configure the Munin monitoring server.                                                                                                                    |    ✅    |
| [`munin_node`](https://github.com/amedee/ansible-servers/tree/main/roles/munin_node)                   | Configure Munin monitoring agents and plugins.                                                                                                                        |    ✅    |
| [`mysql`](https://github.com/amedee/ansible-servers/tree/main/roles/mysql)                             | Install and secure the MySQL database service.                                                                                                                        |    ✅    |
| [`nginx`](https://github.com/amedee/ansible-servers/tree/main/roles/nginx)                             | Install and configure Nginx web hosting.                                                                                                                              |    ✅    |
| [`php`](https://github.com/amedee/ansible-servers/tree/main/roles/php)                                 | Install PHP packages and PHP-FPM modules.                                                                                                                             |    ✅    |
| [`postfix`](https://github.com/amedee/ansible-servers/tree/main/roles/postfix)                         | Configure Postfix mail delivery and filtering.                                                                                                                        |    ✅    |
| [`redis`](https://github.com/amedee/ansible-servers/tree/main/roles/redis)                             | Install and configure the Redis server.                                                                                                                               |    ✅    |
| [`swapfile`](https://github.com/amedee/ansible-servers/tree/main/roles/swapfile)                       | Create and enable a system swapfile.                                                                                                                                  |    ✅    |
| [`unattended_upgrades`](https://github.com/amedee/ansible-servers/tree/main/roles/unattended_upgrades) | Enable automatic APT updates and upgrades.                                                                                                                            |    ✅    |
| [`wp`](https://github.com/amedee/ansible-servers/tree/main/roles/wp)                                   | Deploy and maintain WordPress with plugins and backups.                                                                                                               |    ✅    |
| [`wpcli`](https://github.com/amedee/ansible-servers/tree/main/roles/wpcli)                             | Install and verify the WP-CLI executable.                                                                                                                             |    ✅    |

<!-- molecule-coverage:end -->

[![Deployment Status][deployment-badge]][deployment-status]
[![Super-Linter][superlinter-badge]][superlinter-status]
[![CodeFactor][codefactor-badge]][codefactor-status]
[![pre-commit.ci status][pre-commit-badge]][pre-commit-status]

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
[superlinter-badge]:
  https://github.com/amedee/ansible-servers/actions/workflows/code-quality-super-linter.yml/badge.svg
[superlinter-status]:
  https://github.com/marketplace/actions/code-quality-super-linter
[codefactor-badge]:
  https://www.codefactor.io/repository/github/amedee/ansible-servers/badge
[codefactor-status]:
  https://www.codefactor.io/repository/github/amedee/ansible-servers
[pre-commit-badge]:
  https://results.pre-commit.ci/badge/github/amedee/ansible-servers/main.svg
[pre-commit-status]:
  https://results.pre-commit.ci/latest/github/amedee/ansible-servers/main
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
