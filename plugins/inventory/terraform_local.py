from pathlib import Path
from json import load
from ansible.plugins.inventory import BaseInventoryPlugin
from jinja2 import Template

# See: https://github.com/ansible/ansible/blob/devel/examples/DOCUMENTATION.yml
DOCUMENTATION = """
module: lkummer.homelab.terraform_local
short_description: Construct inventory from local Terraform state
description:
    - Construct inventory from local Terraform state files.
author: "Lior Kummer (@LKummer)"
options:
    tfstate_path:
        description:
            - Path to tfstate file.
        type: string
        required: true
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
    NAME = "lkummer.homelab.terraform_local"

    # For more information on inventory, see:
    # https://github.com/ansible/ansible/blob/stable-2.13/lib/ansible/inventory/data.py
    def parse(self, inventory, loader, path, cache=True):
        # Call base method to ensure properties are available for other methods.
        super().parse(inventory, loader, path, cache)

        config = self._read_config_data(path)
        tfstate_path = Path(config["tfstate_path"])
        with tfstate_path.open(mode="r", encoding="utf-8") as tfstate_file:
            tfstate = load(tfstate_file)
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
