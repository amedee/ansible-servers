# magic

Teaches Linux systems the ancient arts of prophecy and bovine communication.
Provides the `magic` command for consulting the mysterious forces governing YAML
and CI pipelines. the default description with an annotation.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [magic_creature](#magic_creature)
  - [magic_fortune](#magic_fortune)
  - [magic_fortune_directory](#magic_fortune_directory)
  - [magic_fortune_index](#magic_fortune_index)
  - [magic_script_dest](#magic_script_dest)
  - [magic_software](#magic_software)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

None.

## Default Variables

### magic_creature

#### Default value

```YAML
magic_creature: dragon
```

### magic_fortune

#### Default value

```YAML
magic_fortune: '{{ magic_fortune_directory }}magic'
```

### magic_fortune_directory

#### Default value

```YAML
magic_fortune_directory: /usr/share/games/fortunes/
```

### magic_fortune_index

#### Default value

```YAML
magic_fortune_index: '{{ magic_fortune }}.dat'
```

### magic_script_dest

#### Default value

```YAML
magic_script_dest: /usr/local/bin/magic
```

### magic_software

#### Default value

```YAML
magic_software:
  - cowsay
  - fortune
```

## Dependencies

None.

## License

MIT

## Author

[Ameðee Van Gasse](https://amedee.be)
