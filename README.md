# Homelab Ansible Collection

Collection with roles and plugins for automating a virtualized homelab.

Roles:

* `argo` configuring ArgoCD.
* `helm` installing Helm.
* `k3s` configuring K3s.
* `prometheus` configuring Prometheus Operator, Grafana, Loki and Promtail.

Inventory plugins:

* `terraform_local` populating inventory from local Terraform state files.

## Installation

Add the collection to your requirements file.

```yaml
---
collections:
  - name: lkummer.homelab
    type: git
    source: https://github.com/LKummer/ansible-collection-homelab.git
    version: 1.0.0
```

Install with the requirements file.

```
ansible-galaxy collection install --requirements requirements.yaml
```

## Documentation

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
