import csv
import yaml
import os

def generate_ansible_inventory(csv_file_path, output_yaml_path):
    # Load the CSV file
    try:
        with open(csv_file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            devices_data = list(reader)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return

    # Initialize the Ansible inventory structure
    ansible_inventory = {
        'all': {
            'vars': {
                'ansible_user': 'ansible_automation_user',
                'ansible_password': '"{{ vault_ansible_password }}"',
                'ansible_become': 'yes',
                'ansible_become_method': 'enable',
                'ansible_become_pass': '"{{ vault_ansible_enable_password }}"',
                'ansible_network_cli_ssh_type': 'libssh',
                'ansible_command_timeout': 30
            },
            'children': {
                'core': {'children': {}},
                'distribution': {'children': {}},
                'access': {'children': {}}
            }
        }
    }

    # Iterate over rows in the Excel sheet, skipping the header
    for row_data in devices_data:
        hostname = row_data.get('Hostname')
        ansible_host = row_data.get('Ansible_Host')
        vendor = row_data.get('Vendor')
        layer = row_data.get('Layer')

        if not all([hostname, ansible_host, vendor, layer]):
            print(f"Skipping row: Missing required data. Row: {row_data}")
            continue

        # Ensure layer group exists
        if layer not in ansible_inventory['all']['children']:
            ansible_inventory['all']['children'][layer] = {'children': {}}

        # Ensure vendor-specific group under the layer exists
        vendor_layer_group_name = f"{vendor}_{layer}"
        if vendor_layer_group_name not in ansible_inventory['all']['children'][layer]['children']:
            ansible_inventory['all']['children'][layer]['children'][vendor_layer_group_name] = {'hosts': {}}

        # Add the host to the inventory
        ansible_inventory['all']['children'][layer]['children'][vendor_layer_group_name]['hosts'][hostname] = {
            'ansible_host': ansible_host
        }

    # Write the generated inventory to a YAML file
    try:
        with open(output_yaml_path, 'w') as f:
            yaml.dump(ansible_inventory, f, sort_keys=False, indent=2)
        print(f"Ansible inventory successfully generated at {output_yaml_path}")
    except Exception as e:
        print(f"Error writing YAML file: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))

    csv_input_path = os.path.join(project_root, 'inventory', 'network_devices.csv')
    yaml_output_path = os.path.join(project_root, 'inventory', 'inventory.yml')

    generate_ansible_inventory(csv_input_path, yaml_output_path)
