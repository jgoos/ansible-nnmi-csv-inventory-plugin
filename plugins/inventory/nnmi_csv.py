from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleParserError

from csv import DictReader
import re

DOCUMENTATION = r'''
    name: nnmi_csv
    plugin_type: inventory
    short_description: Returns Ansible inventory from CSV
    description: Returns Ansible inventory from NNMi CSV Export
    options:
      plugin:
          description: Name of the plugin
          required: true
          choices: ['nnmi_csv']
      path_to_inventory:
        description: Directory location of the CSV inventory
        required: true
      csv_file:
        description: File name of the CSV inventory file
        required: true
'''

EXAMPLES = r'''
# Sample configuration file for NNMi CSV dynamic inventory
    plugin: nnmi_csv
    path_to_inventory: upload_dir
    csv_file: example.csv
'''

class InventoryModule(BaseInventoryPlugin):

    # used internally by Ansible, it should match the file name but not required
    NAME = 'nnmi_csv'

    def verify_file(self, path):
        ''' return true/false if this is possibly a valid file for this plugin to consume '''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith(('csv_inventory.yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache):
        '''Return dynamic inventory from source '''
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # Read the inventory YAML file
        self._read_config_data(path)

        try:
            # Store the options from the YAML file
            self.plugin = self.get_option('plugin')
            self.inv_dir = self.get_option('path_to_inventory')
            self.inv_file = self.get_option('csv_file')

            self.inventory_file = self.inv_dir + '/' + self.inv_file
        except Exception as e:
            raise AnsibleParserError(
                'All correct options required: {}'.format(e))

        with open(self.inventory_file, 'r') as read_obj:
            dict_reader = DictReader(read_obj)
            list_of_dict = list(dict_reader)

        for line in list_of_dict:
            csv_hostname = line['Hostname']
            csv_group_name = line['Device Family'].lower().replace("-", "_").replace(" ", "_").strip("<>")

            # find the cascade id in system location column
            string_to_search = line['System Location']
            self.cascade_id = re.findall(r'(\b[A-Z]{2,3}-[A-Z]{2,3}-\d{2})', string_to_search, flags=re.IGNORECASE)

            self.inventory.add_group(csv_group_name)
            self.inventory.add_host(csv_hostname)
            self.inventory.set_variable(csv_hostname, 'ansible_hostname', line['Management Address'])
            self.inventory.set_variable(csv_hostname, 'name', line['Name'])
            self.inventory.set_variable(csv_hostname, 'system_location', line['System Location'])
            self.inventory.set_variable(csv_hostname, 'device_family', line['Device Family'])
            self.inventory.set_variable(csv_hostname, 'device_category', line['Device Category'])
            self.inventory.set_variable(csv_hostname, 'system_description', line['System Description'])
            self.inventory.add_child(csv_group_name, csv_hostname)
            if self.cascade_id:
                self.inventory.set_variable(csv_hostname, 'cascade_id', self.cascade_id[0])

            ansible_network_os_mapping = {
                'Cisco Adaptive Security Appliance': 'asa',
                'Cisco NX-OS': 'nxos',
                'Cisco IOS Software': 'ios',
                'Cisco IOS XR Software': 'iosxr',
            }

            for entry in ansible_network_os_mapping.keys():
                if str(entry) in line['System Description']:
                    self.inventory.set_variable(csv_hostname, 'ansible_network_os', ansible_network_os_mapping[entry])
