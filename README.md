# Ansible NNMi CSV Inventory Plugin

The inventory plugin reads a NNMi CSV export with network devices and converts this to an ansible inventory. Network devices will be grouped by type.

What is NNMi? 
NNMi is a network management software provided by Microfocus, which provides visibility into the performance and availability of network devices. The CSV export contains information about the devices managed by NNMi.

## Configuring the plugin

1. Create a config file:

``` yaml
---
# example nnmi_csv_inventory.yaml
plugin: nnmi_csv
path_to_inventory: <csv_inventory> # Directory location of CSV
csv_file: <csv_file>               # Name of the CSV file
```

2. Create an ansible.cfg
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

## File & directory structure:

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

## Usage

Example usage of ansible-inventory command:

`ansible-inventory --list`

## Troubleshoot

If you are facing any errors, please make sure that

-   File and directory structure is followed as mentioned above
-   Correct path and file name is provided in the nnmi_csv_inventory.yml
-   ansible.cfg is updated correctly with the required details

