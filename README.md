# Network Automation with Ansible (Multi-Vendor & Layered)

This project provides a comprehensive Ansible-based solution for automating various tasks across a multi-vendor network environment, including Cisco, MikroTik, Huawei, H3C, and ZTE devices. It now incorporates a layered network design (Core, Distribution, Access) and uses a dynamic inventory generated from an Excel (CSV) file, along with vendor-specific credentials.

## Project Structure

```
network_automation/
├── inventory/
│   ├── inventory.yml
│   └── network_devices.csv
├── group_vars/
│   ├── all.yml
│   ├── core.yml
│   ├── distribution.yml
│   ├── access.yml
│   ├── cisco.yml
│   ├── mikrotik.yml
│   ├── huawei.yml
│   ├── h3c.yml
│   ├── zte.yml
│   └── vault.yml
├── host_vars/ (for device-specific variables)
├── playbooks/
│   ├── backup_configs.yml
│   ├── collect_logs.yml
│   ├── health_check.yml
│   ├── interface_status.yml
│   ├── configure_snmp.yml
│   ├── apply_changes.yml
│   ├── compliance_check.yml
│   ├── firmware_upgrade.yml
│   └── gather_cisco_facts.yml
├── roles/
│   └── common/
│       ├── tasks/
│       │   ├── configure_ntp.yml
│       │   ├── ios_ntp.yml
│       │   ├── community.routeros.routeros_ntp.yml
│       │   ├── huawei.os.vrp_ntp.yml
│       │   ├── h3c.comware.comware_ntp.yml
│       │   └── zte.zxros.zxros_ntp.yml
│       ├── handlers/
│       ├── templates/
│       └── vars/
├── scripts/
│   ├── run_backup.sh
│   ├── run_log_collection.sh
│   └── excel_to_ansible_inventory.py
├── cron_jobs/
│   └── weekly_backup.cron
├── backups/ (created by backup_configs.yml)
├── logs/ (created by collect_logs.yml)
├── health_checks/ (created by health_check.yml)
├── interface_status/ (created by interface_status.yml)
├── compliance_reports/ (created by compliance_check.yml)
├── reports/ (for generated reports like cisco_router_1_report.html)
├── templates/ (for apply_changes.yml and report_template.html)
│   ├── ios_changes.j2
│   ├── community.routeros.routeros_changes.j2
│   ├── huawei.os.vrp_changes.j2
│   ├── h3c.comware.comware_changes.j2
│   ├── zte.zxros.zxros_changes.j2
│   └── report_template.html
└── compliance_rules/ (for compliance_check.yml)
    ├── ios_rules.yml
    ├── community.routeros.routeros_rules.yml
    ├── huawei.os.vrp_rules.yml
    ├── h3c.comware.comware_rules.yml
    └── zte.zxros.zxros_rules.yml

```

## Setup and Usage

### 1. Prerequisites

- Ansible installed on your control machine.
- Python installed on your control machine.
- Python libraries: `openpyxl` (if using .xlsx), `pyyaml`, `jinja2`. Install with `sudo pip3 install openpyxl pyyaml Jinja2`.
- Network modules for each vendor installed (e.g., `cisco.ios`, `community.routeros`, `huawei.os`, `h3c.comware`, `zte.zxros`). You can install them using `ansible-galaxy collection install <collection_name>`.
  - `ansible-galaxy collection install cisco.ios`
  - `ansible-galaxy collection install community.routeros`
  - `ansible-galaxy collection install huawei.os`
  - `ansible-galaxy collection install h3c.comware`
  - `ansible-galaxy collection install zte.zxros`
- SSH access to your network devices with appropriate credentials.

### 2. Inventory Configuration (`inventory/network_devices.csv` and `inventory/inventory.yml`)

Instead of manually editing `inventory.yml`, you will manage your network device inventory using `network_devices.csv` and generate the `inventory.yml` file from it.

**`inventory/network_devices.csv` Format**:

Create or edit the `network_devices.csv` file with the following columns:

| Hostname             | Ansible_Host  | Vendor     | Layer        |
| :------------------- | :------------ | :--------- | :----------- |
| `core_cisco_router_1`| `192.168.10.1`| `cisco`    | `core`       |
| `dist_mikrotik_sw_1` | `192.168.20.2`| `mikrotik` | `distribution`|
| `access_huawei_ap_1` | `192.168.30.3`| `huawei`   | `access`     |

*   **Hostname**: Unique name for the device (e.g., `core_cisco_router_1`).
*   **Ansible_Host**: IP address or FQDN of the device.
*   **Vendor**: `cisco`, `mikrotik`, `huawei`, `h3c`, `zte` (must match `group_vars` filenames).
*   **Layer**: `core`, `distribution`, `access` (must match `group_vars` filenames).

**Generating `inventory.yml` from CSV**:

Run the provided Python script to convert your CSV data into the Ansible YAML inventory format:

```bash
python3 scripts/excel_to_ansible_inventory.py
```

This will create/update `inventory/inventory.yml` based on your `network_devices.csv` file. The script automatically creates layer-based and vendor-specific groups (e.g., `core`, `cisco_core`, `distribution`, `mikrotik_distribution`, etc.).

### 3. Group Variables (`group_vars/`)

Vendor-specific connection settings and common variables are defined in `group_vars/`. These files now also contain placeholders for credentials, which should be managed using Ansible Vault.

*   **`group_vars/all.yml`**: Contains global variables applicable to all devices. It now uses `vault_ansible_password` and `vault_ansible_enable_password` for common credentials.
*   **`group_vars/core.yml`, `group_vars/distribution.yml`, `group_vars/access.yml`**: These files are for variables specific to each network layer. You can add layer-specific settings here.
*   **`group_vars/cisco.yml`, `group_vars/mikrotik.yml`, `group_vars/huawei.yml`, `group_vars/h3c.yml`, `group_vars/zte.yml`**: These files contain vendor-specific network OS definitions and placeholders for vendor-specific usernames and passwords (e.g., `vault_cisco_password`).
*   **`group_vars/vault.yml`**: This file contains all the `vault_` prefixed variables for sensitive credentials. **You MUST encrypt this file using Ansible Vault.**

**Example `group_vars/vault.yml` (before encryption)**:

```yaml
vault_ansible_password: "your_global_ansible_password"
vault_ansible_enable_password: "your_global_enable_password"
vault_cisco_password: "your_cisco_password"
vault_cisco_enable_password: "your_cisco_enable_password"
vault_mikrotik_password: "your_mikrotik_password"
vault_huawei_password: "your_huawei_password"
vault_huawei_enable_password: "your_huawei_enable_password"
vault_h3c_password: "your_h3c_password"
vault_h3c_enable_password: "your_h3c_enable_password"
vault_zte_password: "your_zte_password"
vault_zte_enable_password: "your_zte_enable_password"
```

**Encrypting `vault.yml`**: Use `ansible-vault encrypt group_vars/vault.yml` to encrypt this file. You will be prompted to set a vault password. When running playbooks, you will need to provide this vault password (e.g., using `--ask-vault-pass` or `--vault-password-file`).

### 4. Playbooks

All playbooks (`.yml` files in the `playbooks/` directory) are designed to work with the new `inventory.yml` structure. They typically target `hosts: all` and use the `ansible_network_os` variable (which is dynamically set based on the vendor group) to apply vendor-specific tasks.

- **`backup_configs.yml`**: Backs up running configurations of all devices to `./backups/<hostname>/`.
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/backup_configs.yml --ask-vault-pass`
- **`collect_logs.yml`**: Collects logs from all devices and saves them to `./logs/<hostname>/`.
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/collect_logs.yml --ask-vault-pass`
- **`health_check.yml`**: Performs various health checks (version, CPU, memory, environment) and saves output to `./health_checks/<hostname>/`.
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/health_check.yml --ask-vault-pass`
- **`interface_status.yml`**: Collects interface status and saves output to `./interface_status/<hostname>/`.
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/interface_status.yml --ask-vault-pass`
- **`configure_snmp.yml`**: Configures basic SNMP settings (read-only community, traps) on devices.
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/configure_snmp.yml --ask-vault-pass`
- **`apply_changes.yml`**: Applies configuration changes from templates located in `templates/`.
  - **Before running**: Create a Jinja2 template for each vendor (e.g., `templates/ios_changes.j2`) with the desired configuration lines.
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/apply_changes.yml --ask-vault-pass`
- **`compliance_check.yml`**: Checks device configurations against defined compliance rules.
  - **Before running**: Create compliance rules files for each vendor (e.g., `compliance_rules/ios_rules.yml`).
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/compliance_check.yml --ask-vault-pass`
- **`firmware_upgrade.yml`**: Facilitates firmware upgrades. **Use with extreme caution and thorough testing.**
  - **Before running**: Place firmware images in the specified `firmware_image_path` and update `firmware_image_name` variables.
  - MikroTik firmware upgrade often requires specific manual steps or custom scripts due to its unique upgrade process.
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/firmware_upgrade.yml --ask-vault-pass`
- **`gather_cisco_facts.yml`**: Gathers Cisco device facts and saves them as JSON to `./reports/`.
  - To run: `ansible-playbook -i inventory/inventory.yml playbooks/gather_cisco_facts.yml --ask-vault-pass`

### 5. Roles

Roles organize tasks, handlers, templates, and variables in a reusable structure.

- **`common` role**: Contains common tasks applicable across multiple vendors.
  - **`configure_ntp.yml`**: Configures NTP servers on devices. You need to define `ntp_server_primary` and `ntp_server_secondary` in `group_vars/all.yml` or `host_vars/`.
  - To use in a playbook:
    ```yaml
    - name: Apply common configurations
      hosts: all
      roles:
        - common
      vars:
        ntp_server_primary: 1.pool.ntp.org
        ntp_server_secondary: 2.pool.ntp.org
    ```

### 6. Scheduled Tasks (Cron Jobs)

Scripts are provided to run playbooks, which can then be scheduled using cron.

- **`scripts/run_backup.sh`**: Executes the `backup_configs.yml` playbook.
- **`scripts/run_log_collection.sh`**: Executes the `collect_logs.yml` playbook.

To schedule the weekly config backup, add the content of `cron_jobs/weekly_backup.cron` to your crontab:

```bash
crontab -e
```

Then add the line:

```cron
0 2 * * 0 /home/ubuntu/network_automation/scripts/run_backup.sh >> /home/ubuntu/network_automation/logs/backup_cron.log 2>&1
```

This will run the backup script every Sunday at 2:00 AM, logging output to `backup_cron.log`.

## Security Considerations

- **Ansible Vault**: **Always use Ansible Vault to encrypt sensitive data like passwords and API keys.** The `group_vars/vault.yml` file is specifically designed for this. Never store plain-text credentials in your repository.
- **Least Privilege**: Configure network devices with minimal necessary privileges for the Ansible user.
- **SSH Keys**: Prefer SSH key-based authentication over password-based authentication.

## Further Enhancements

- **Error Handling**: Implement more robust error handling and notification mechanisms.
- **Reporting**: Generate detailed reports for compliance checks, health checks, and configuration changes.
- **Version Control**: Integrate with Git for tracking configuration changes and backups.
- **Dynamic Inventory**: Explore advanced dynamic inventory sources beyond CSV if your infrastructure is highly dynamic.
- **CI/CD Integration**: Integrate Ansible playbooks into a CI/CD pipeline for automated testing and deployment.

This updated framework provides a robust and flexible foundation for network automation, catering to multi-vendor environments with layered designs and secure credential management. Customize and expand upon it to fit your specific network environment and operational needs.
