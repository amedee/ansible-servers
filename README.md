# ansible-servers

Ansible playbooks to configure my servers

Deploy with

```shell
ansible-playbook playbooks/site.yml
```

[![Deployment Status][badge]][deployment]

## References

* The Postfix [checks files][checks files] are retrieved from the
  [Web Archive of securitysage.com][securitysage].
  Last retrieval date: 6 January 2007.

[badge]:        https://github.com/amedee/ansible-servers/actions/workflows/ansible-deploy.yml/badge.svg
[deployment]:   https://github.com/amedee/ansible-servers/actions/workflows/ansible-deploy.yml
[checks files]: roles/mailserver/files/checks
[securitysage]: https://web.archive.org/web/20070106001401/http://www.securitysage.com:80/guides/postfix_uce.html
