# Homelab Ansible Collection

Collection with roles and plugins for automating a virtualized homelab.

Roles:

* `lkummer.homelab.argo` configuring ArgoCD.
* `lkummer.homelab.helm` installing Helm.
* `lkummer.homelab.k3s` configuring K3s.
* `lkummer.homelab.prometheus` configuring Prometheus Operator, Grafana, Loki and Promtail.

Inventory plugins:

* `lkummer.homelab.terraform_local` populating inventory from local Terraform state files.

## Example

Included roles are designed to work together to configure a single host Kubernetes cluster with metric collection, log aggregation and continuous delivery.

```yaml
---
- name: Configure Kubernetes host
  hosts: production
  roles:
    - role: lkummer.homelab.k3s
    - role: lkummer.homelab.helm
    - role: lkummer.homelab.prometheus
      vars:
        prometheus_grafana_host: grafana.example.com
        prometheus_grafana_user: admin
        prometheus_grafana_password: admin
    - role: lkummer.homelab.argo
      vars:
        argo_host: argo.example.com
        argo_cert_manager_enabled: false
```

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
