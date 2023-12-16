resource "random_uuid" "id" {
}

module "machine" {
  source = "github.com/LKummer/terraform-proxmox//modules/machine?ref=4.0.0"

  proxmox_api_url  = var.proxmox_api_url
  proxmox_template = var.proxmox_template

  name            = "ansible-homelab-test-${random_uuid.id.result}"
  description     = "Created by ansible-collection-homelab automated testing suite."
  on_boot         = true
  memory          = 6 * 1024
  cores           = 4
  disk_pool       = "local-lvm"
  disk_size       = 10
  authorized_keys = [var.cloud_init_public_keys]
}
