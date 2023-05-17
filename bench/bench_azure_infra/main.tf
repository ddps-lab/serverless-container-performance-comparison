provider "azurerm" {
  features {}
}

# resource "azurerm_resource_group" "bench-resource-group" {
#   name = "${var.prefix}-scpc-bench-resourcees"
#   location = var.location
# }

data "azurerm_resource_group" "bench-resource-group" {
  name = var.resource_group_name
}

data "azurerm_ssh_public_key" "ssh-key" {
  name = var.ssh-keyname
  resource_group_name = data.azurerm_resource_group.bench-resource-group.name
}