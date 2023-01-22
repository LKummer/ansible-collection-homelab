resource "random_uuid" "id" {
}

module "machine" {
  source = "github.com/LKummer/terraform-proxmox//modules/machine?ref=1.0.0"

  proxmox_api_url     = var.proxmox_api_url
  proxmox_target_node = var.proxmox_target_node
  proxmox_template    = var.proxmox_template

  name                   = "ansible-homelab-test-${random_uuid.id.result}"
  description            = "Created by ansible-collection-homelab automated testing suite."
  on_boot                = true
  memory                 = 4096
  cores                  = 4
  disk_pool              = "local-lvm"
  disk_size              = "10G"
  cloud_init_public_keys = var.cloud_init_public_keys
}