# ansible-servers

Ansible playbooks to configure my servers:

- [amedee.be]: based on DigitalOcean's [1-Click LEMP Droplet][lemp droplet]
- [box.vangasse.eu]: Standard Ubuntu 22.04 LTS droplet with [Mail-in-a-Box][mailinabox]

Deploy with

```shell
ansible-playbook playbooks/site.yml
```

[![Deployment Status][deployment-badge]][deployment-status]
[![Codacy Badge][codacy-badge]][codacy-grade]
[![Super-Linter][superlinter-badge]][superlinter-status]
[![CodeFactor][codefactor-badge]][codefactor-status]
[![License: MIT][license-badge]][license-link]

## 🔍 Repository History

[![Gource thumbnail][gource-thumbnail]][gource-video]

> Click to watch a timelapse of this repository’s evolution.

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
