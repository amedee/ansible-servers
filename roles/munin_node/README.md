# munin_node

Configure Munin monitoring agents and plugins.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [munin_node_allowed_ips](#munin_node_allowed_ips)
  - [munin_node_bind_host](#munin_node_bind_host)
  - [munin_node_bind_port](#munin_node_bind_port)
  - [munin_node_config](#munin_node_config)
  - [munin_node_host_name](#munin_node_host_name)
  - [munin_node_install_plugins](#munin_node_install_plugins)
  - [munin_node_plugin_dest_path](#munin_node_plugin_dest_path)
  - [munin_node_plugin_src_path](#munin_node_plugin_src_path)
  - [munin_node_plugins](#munin_node_plugins)
  - [munin_node_server_ip](#munin_node_server_ip)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.21`

## Default Variables

### munin_node_allowed_ips

#### Default value

```YAML
munin_node_allowed_ips:
  - ^127\.0\.0\.1$
  - ^::1$
```

### munin_node_bind_host

#### Default value

```YAML
munin_node_bind_host: '*'
```

### munin_node_bind_port

#### Default value

```YAML
munin_node_bind_port: '4949'
```

### munin_node_config

#### Default value

```YAML
munin_node_config: {}
```

### munin_node_host_name

#### Default value

```YAML
munin_node_host_name: ''
```

### munin_node_install_plugins

#### Default value

```YAML
munin_node_install_plugins: []
```

### munin_node_plugin_dest_path

#### Default value

```YAML
munin_node_plugin_dest_path: /etc/munin/plugins/
```

### munin_node_plugin_src_path

#### Default value

```YAML
munin_node_plugin_src_path: /usr/share/munin/plugins/
```

### munin_node_plugins

#### Default value

```YAML
munin_node_plugins: []
```

### munin_node_server_ip

#### Default value

```YAML
munin_node_server_ip: 142.93.227.16
```

## Dependencies

None.

## License

MIT

## Author

[Ameðea Van Gasse](https://amedee.be)
