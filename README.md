# Net Command

## 简介

Net Command 是一个用于并行执行网络设备命令的工具，支持通过 playbook 文件定义任务。

## 安装

```sh
poetry install
```

## 使用方法

### 运行命令

```sh
poetry run netcmd -i <inventory_file> <playbook_file>
```

### 列出清单

```sh
poetry run netcmd -i <inventory_file> --list
```

## 配置文件

### Inventory 文件

Inventory 文件定义了网络设备的分组和变量。示例：

```yaml
all:
  vars:
    user: admin
    password: admin
    port: 22

box_as:
  hosts:
    192.168.56.3:
      vendor: hp_comware
    192.168.56.4:
      vendor: hp_comware
```

### Playbook 文件

Playbook 文件定义了要执行的任务。示例：

```yaml
- name: H3C NTP Configuration
  hosts: box_as
  num_processes: 2
  vars:
    host: "{{ host }}"
    port: "{{ port }}"
    username: "{{ user }}"
    password: "{{ password }}"
  tasks:
    - name: Display H3C Commands
      when: vendor == 'hp_comware'
      display_commands: 
        - display ntp status
        - display clock

    - name: H3C Config Commands
      when: vendor == 'hp_comware'
      config_commands: 
        - acl basic 2100
        - rule 5 permit
        - quit
        - save force
```

## 日志

日志文件保存在 `logs/` 目录下，每个设备对应一个日志文件。

## 贡献

欢迎提交问题和贡献代码！
