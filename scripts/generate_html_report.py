import json
from jinja2 import Environment, FileSystemLoader
import os

def generate_report(json_file_path, template_path, output_dir):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    hostname = data['ansible_facts']['ansible_net_hostname']
    model = data['ansible_facts']['ansible_net_model']
    version = data['ansible_facts']['ansible_net_version']
    serial_number = data['ansible_facts']['ansible_net_serialnum']
    interfaces = data['ansible_facts']['ansible_net_interfaces']

    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    rendered_html = template.render(
        hostname=hostname,
        model=model,
        version=version,
        serial_number=serial_number,
        interfaces=interfaces
    )

    output_file_path = os.path.join(output_dir, f"{hostname}_report.html")
    with open(output_file_path, 'w') as f:
        f.write(rendered_html)
    print(f"Report generated: {output_file_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))

    json_data_path = os.path.join(project_root, 'reports', 'cisco_router_1_facts.json')
    html_template_path = os.path.join(project_root, 'templates', 'report_template.html')
    output_reports_dir = os.path.join(project_root, 'reports')

    generate_report(json_data_path, html_template_path, output_reports_dir)
