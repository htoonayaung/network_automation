# Network Automation System - အသုံးပြုပုံ လမ်းညွှန် (Manual Book)

ဤလမ်းညွှန်ချက်သည် Cisco, MikroTik, Huawei, H3C, နှင့် ZTE vendor များပါဝင်သော Network Automation System ကို အဆင့်ဆင့် အသုံးပြုပုံနှင့် ပြင်ဆင်ပုံများကို ရှင်းပြထားပါသည်။

---

## အပိုင်း (၁) - ကြိုတင်ပြင်ဆင်ရန် လိုအပ်ချက်များ (Prerequisites)

စနစ်ကို မစတင်မီ အောက်ပါတို့ ရှိနေရန် လိုအပ်ပါသည်။

1.  **Ansible Control Machine**: Linux (Ubuntu/CentOS) သို့မဟုတ် macOS ရှိသော ကွန်ပျူတာ။
2.  **Python 3**: Python 3 နှင့် လိုအပ်သော library များ (pip ဖြင့် install လုပ်ပါ)။
    ```bash
    sudo pip3 install openpyxl pyyaml Jinja2
    ```
3.  **Ansible Collections**: Vendor အလိုက် လိုအပ်သော collection များကို install လုပ်ပါ။
    ```bash
    ansible-galaxy collection install cisco.ios community.routeros huawei.os h3c.comware zte.zxros
    ```
4.  **Network Connectivity**: Control machine မှ network device များသို့ SSH ဖြင့် ချိတ်ဆက်နိုင်ရပါမည်။

---

## အပိုင်း (၂) - Device စာရင်း ထည့်သွင်းခြင်း (Inventory Management)

Device အသစ်များ ထည့်ရန် သို့မဟုတ် ရှိပြီးသား device များကို ပြင်ဆင်ရန် `inventory/network_devices.csv` ဖိုင်ကို အသုံးပြုရပါမည်။

### အဆင့် (၁) - CSV ဖိုင်ကို ပြင်ဆင်ခြင်း
`inventory/network_devices.csv` ကို Excel သို့မဟုတ် Text Editor ဖြင့် ဖွင့်ပြီး အောက်ပါအတိုင်း ဖြည့်စွက်ပါ။

| Hostname | Ansible_Host | Vendor | Layer |
| :--- | :--- | :--- | :--- |
| Core_R1 | 10.0.0.1 | cisco | core |
| Dist_SW1 | 10.0.0.2 | mikrotik | distribution |
| Access_SW1 | 10.0.0.3 | huawei | access |

*   **Vendor**: `cisco`, `mikrotik`, `huawei`, `h3c`, `zte` ဟုသာ ရေးရပါမည်။
*   **Layer**: `core`, `distribution`, `access` ဟုသာ ရေးရပါမည်။

### အဆင့် (၂) - Ansible Inventory ထုတ်လုပ်ခြင်း
CSV ပြင်ပြီးပါက အောက်ပါ command ကို run ပါ။ ၎င်းသည် `inventory/inventory.yml` ကို အလိုအလျောက် update လုပ်ပေးပါမည်။
```bash
python3 scripts/excel_to_ansible_inventory.py
```

---

## အပိုင်း (၃) - Password နှင့် Username များ သတ်မှတ်ခြင်း (Credentials)

လုံခြုံရေးအတွက် Password များကို `group_vars/vault.yml` တွင် သိမ်းဆည်းရပါမည်။

### အဆင့် (၁) - Password များ ဖြည့်သွင်းခြင်း
`group_vars/vault.yml` ကို ဖွင့်ပြီး သက်ဆိုင်ရာ vendor အလိုက် username/password များကို ပြင်ဆင်ပါ။

### အဆင့် (၂) - Ansible Vault ဖြင့် Encrypt လုပ်ခြင်း
Password ဖိုင်ကို သူများမမြင်နိုင်အောင် encrypt လုပ်ပါ။
```bash
ansible-vault encrypt group_vars/vault.yml
```
(Password တစ်ခု သတ်မှတ်ခိုင်းပါလိမ့်မည်။ ထို password ကို မှတ်ထားပါ။)

---

## အပိုင်း (၄) - Playbook များ အသုံးပြုခြင်း (Running Tasks)

Automation task များကို run ရန် `ansible-playbook` command ကို အသုံးပြုရပါမည်။

### ၁။ Config Backup ယူခြင်း
```bash
ansible-playbook -i inventory/inventory.yml playbooks/backup_configs.yml --ask-vault-pass
```
(Vault password ကို ရိုက်ထည့်ပေးရပါမည်။)

### ၂။ Log များ စုစည်းခြင်း
```bash
ansible-playbook -i inventory/inventory.yml playbooks/collect_logs.yml --ask-vault-pass
```

### ၃။ Health Check စစ်ဆေးခြင်း
```bash
ansible-playbook -i inventory/inventory.yml playbooks/health_check.yml --ask-vault-pass
```

---

## အပိုင်း (၅) - လိုအပ်သလို ပြင်ဆင်ခြင်း (Customization)

### ၁။ Vendor အလိုက် Variable များ ပြင်ဆင်ခြင်း
Vendor တစ်ခုချင်းစီအတွက် သီးသန့် setting များ (ဥပမာ - SSH port, timeout) ကို `group_vars/<vendor_name>.yml` တွင် ပြင်နိုင်ပါသည်။

### ၂။ Configuration Changes Template များ ပြင်ခြင်း
Device များထဲသို့ config အသစ်များ ထည့်လိုပါက `templates/` အောက်ရှိ `.j2` ဖိုင်များတွင် သွားရောက်ရေးသားနိုင်ပါသည်။
*   ဥပမာ - Cisco အတွက် `templates/ios_changes.j2` တွင် config line များ ရေးပါ။
*   ပြီးနောက် `playbooks/apply_changes.yml` ကို run ပါ။

---

## အပိုင်း (၆) - အချိန်ဇယားဖြင့် ခိုင်းစေခြင်း (Scheduling)

အပတ်စဉ် တနင်္ဂနွေနေ့တိုင်း Backup အလိုအလျောက် ယူစေလိုပါက:

1.  `scripts/run_backup.sh` ထဲရှိ path လမ်းကြောင်းများ မှန်မမှန် စစ်ဆေးပါ။
2.  Crontab တွင် အောက်ပါအတိုင်း ထည့်သွင်းပါ။
    ```bash
    crontab -e
    ```
    (အောက်ပါစာကြောင်းကို အောက်ဆုံးတွင် ထည့်ပါ)
    ```cron
    0 2 * * 0 /home/ubuntu/network_automation/scripts/run_backup.sh >> /home/ubuntu/network_automation/logs/backup_cron.log 2>&1
    ```

---

## အပိုင်း (၇) - ပြဿနာဖြေရှင်းခြင်း (Troubleshooting)

*   **Connection Error**: SSH key သို့မဟုတ် Password မှားနေခြင်း ရှိမရှိ စစ်ဆေးပါ။ Device ဘက်တွင် SSH ဖွင့်ထားရန် လိုအပ်ပါသည်။
*   **Module Missing**: လိုအပ်သော Ansible Collection များ install လုပ်ထားခြင်း ရှိမရှိ စစ်ဆေးပါ။
*   **Python Error**: `openpyxl` သို့မဟုတ် `pyyaml` library များ ရှိမရှိ စစ်ဆေးပါ။

---
**Manus AI မှ ဖန်တီးပေးထားသော Network Automation Manual Book ဖြစ်ပါသည်။**
