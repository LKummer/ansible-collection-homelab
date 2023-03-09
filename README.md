# Homelab Ansible Collection

Collection with roles and plugins for automating a virtualized homelab.

Roles:

* `lkummer.homelab.argo` configures ArgoCD.
* `lkummer.homelab.cert_manager` configures Cert Manager and a ClusterIssuer using Let's Encrypt and Cloudflare DNS.
* `lkummer.homelab.k3s` configures K3s.
* `lkummer.homelab.observability` configures Prometheus Operator, Grafana Agent, Grafana, Loki, Promtail, OpenTelemetry Operator, OpenTelemetry Collector and Tempo.
* `lkummer.homelab.helm` configures hosts for use with `kubernetes.core.helm` and `kubernetes.core.k8s` modules.

Inventory plugins:

* `lkummer.homelab.terraform_local` populates inventory from local Terraform state files.
* `lkummer.homelab.terraform_http` populates inventory from http Terraform state backend.

## Example

Included roles are designed to work together to configure a single host Kubernetes cluster with metric collection, log aggregation and continuous delivery.

```yaml
---
- name: Configure Kubernetes host
  hosts: production
  roles:
    - role: lkummer.homelab.k3s
    - role: lkummer.homelab.observability
      vars:
        observability_grafana_host: grafana.example.com
        observability_grafana_user: admin
        observability_grafana_password: admin
    - role: lkummer.homelab.argo
      vars:
        argo_host: argo.example.com
        argo_cert_manager_enabled: false
```

## Installation

Add the collection to the `requirements.yml` file at the root directory of your playbook.

```yaml
# Inside requirements.yml
---
collections:
  - name: lkummer.homelab
    type: git
    source: https://github.com/LKummer/ansible-collection-homelab.git
    version: 3.0.0
```

Install requirements from the file:

```
ansible-galaxy collection install --requirements requirements.yml
```

## Documentation

[Full documentation is available on the wiki](https://homelab.pages.houseofkummer.com/devops/wiki/).
The following instructions are for accessing less detailed documentation from the roles and plugins.

For role variable documentation, see:

```
ansible-doc --type role <role name>
```

For example:

```
ansible-doc --type role lkummer.homelab.k3s
```

For inventory plugin documentation, see:

```
ansible-doc --type inventory lkummer.homelab.terraform_local
```

## Development

This project uses Poetry to manage dependencies in a virtual environment.

Install Poetry as it is required to download development dependencies:

To install Poetry, run:

```
pip install poetry
```

To install development dependencies, run:

```
poetry install
```

Commands must run inside `poetry shell` or using `poetry run` because everything required for
development is installed in a virtual environment, including Ansible, Molecule, and the linters.

To activate the virtual environment, run:

```
poetry shell
```

Or use `poetry run` without activating the virtual environment.
This example runs `ansible-lint`:

```
poetry run ansible-lint -P production
```

### Testing

`PM_API_TOKEN_ID` and `PM_API_TOKEN_SECRET` must be set.
Make sure the token id is of the form `user@pve!token` and contains your username, realm and token name.
Make sure the token has enough privileges for cloning VMs.
[For more information see this guide.](https://homelab.pages.houseofkummer.com/devops/wiki/how-to/proxmox-api-tokens/)

Set `ANSIBLE_HOST_KEY_CHECKING=0` to prevent Ansible from bugging you about SSH host key verification.

Each user facing role (`k3s`, `observability`, `argo`, `cert_manager`) has a Molecule test.
To run a test, first go to the directory of the role you want to test:

```
cd roles/observability
```

Then run Molecule with the following command:

```
molecule test
```

It is useful to run Molecule stages during role development, using the test as a machine and playbook for development.

To provision a machine for testing, run:

```
molecule create
```

To run the playbook of the role, run:

```
molecule converge
```

To run the test verification playbook, run:

```
molecule verify
```

To destroy infrastructure provisioned for the test, run:

```
molecule destroy
```

### Linting

Make sure to lint with both yamllint and ansible-lint before pushing.

To lint with `yamllint`, run:

```
yamllint .
```

To lint with `ansible-lint`, run:

```
ansible-lint -P production
```
