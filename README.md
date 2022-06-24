# ansible NNMi csv inventory plugin

The inventory plugin reads a NNMi CSV export with network devices and converts this to an ansible inventory.
Network devices will be grouped by type.

## Configure

- Create a config file:

``` yaml
---
# example nnmi_csv_inventory.yaml
plugin: nnmi_csv
path_to_inventory: <csv_inventory> # Directory location of CSV
csv_file: <csv_file>               # Name of the CSV file
```

- Create an ansible.cfg
  - Add the yaml config file as a inventory source to the ansible.cfg
  - Add the plugin directory
  - Enable the nnmi_csv plugin

Example ansible.cfg:

``` ini
[defaults]
inventory = nnmi_csv_inventory.yml
inventory_plugins = plugins/inventory

[inventory]
enable_plugins = nnmi_csv
```

File & directory structure:

``` shell
.
├── README.md
├── ansible.cfg
├── inventory
│   └── nnmi_csv_inventory.yml
└── plugins
    └── inventory
        └── nnmi_csv.py
```

## Test

``` shell
ansible-inventory --list
```
