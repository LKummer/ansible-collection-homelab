from ansible.plugins.inventory import AnsibleParserError, BaseInventoryPlugin, os
from jinja2 import Template
import requests

# See: https://github.com/ansible/ansible/blob/devel/examples/DOCUMENTATION.yml
DOCUMENTATION = """
module: lkummer.homelab.terraform_http
short_description: Construct inventory from http Terraform state backend.
description:
    - Construct inventory from http Terraform state backend.
    - Uses TF_HTTP_ADDRESS, TF_HTTP_USERNAME, TF_HTTP_PASSWORD as described
    - here: https://www.terraform.io/language/settings/backends/http#configuration-variables
author: "Lior Kummer (@LKummer)"
options:
    hosts:
        description:
            - List of hosts to add.
            - All values accept template strings, which are rendered with Terraform outputs as context.
        type: list
        elements: dict
        default: []
        suboptions:
            ansible_host:
                description:
                    - IP for SSH connection to the host.
                type: str
                required: true
            ansible_port:
                description:
                    - Port for SSH connection to the host.
                type: str
                required: true
            ansible_group:
                description:
                    - Group to add the host to.
                type: str
                required: true
            vars:
                description:
                    - Extra variables to set on the host.
                type: dict
                default: {}
notes: []
requirements: []
"""


class InventoryModule(BaseInventoryPlugin):
    NAME = "lkummer.homelab.terraform_http"

    # For more information on inventory, see:
    # https://github.com/ansible/ansible/blob/stable-2.13/lib/ansible/inventory/data.py
    def parse(self, inventory, loader, path, cache=True):
        # Call base method to ensure properties are available for other methods.
        super().parse(inventory, loader, path, cache)

        config = self._read_config_data(path)

        tfstate_address = os.getenv("TF_HTTP_ADDRESS")
        tfstate_username = os.getenv("TF_HTTP_USERNAME")
        tfstate_password = os.getenv("TF_HTTP_PASSWORD")

        response = requests.get(
            str(tfstate_address), auth=(str(tfstate_username), str(tfstate_password))
        )
        if response.status_code != 200:
            raise AnsibleParserError(
                f"Terraform state backend '{tfstate_address}' returned status {response.status_code} (not 200)."
            )
        tfstate = response.json()

        # Terraform outputs are stored as {value, type} dicts, this flattens to values.
        template_context = {
            key: value["value"] for key, value in tfstate["outputs"].items()
        }
        for host in config["hosts"]:
            ansible_host = Template(host["ansible_host"]).render(template_context)
            ansible_port = Template(host["ansible_port"]).render(template_context)
            ansible_group = Template(host["ansible_group"]).render(template_context)

            # Add group before adding host, as adding host with unknown group will
            # silently fail.
            inventory.add_group(ansible_group)
            inventory.add_host(ansible_host, ansible_group, ansible_port)

            # Add variables from vars key.
            for key, value in host["vars"].items():
                rendered_value = Template(value).render(template_context)
                inventory.set_variable(ansible_host, key, rendered_value)
