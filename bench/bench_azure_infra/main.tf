provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "bench-resource-group" {
  name = var.resource_group_name
}

data "azurerm_ssh_public_key" "ssh-key" {
  name = var.ssh-keyname
  resource_group_name = data.azurerm_resource_group.bench-resource-group.name
}