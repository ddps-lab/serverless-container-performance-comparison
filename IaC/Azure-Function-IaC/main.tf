provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "bench-resource-group" {
  name = var.resource_group_name
}

data "azurerm_container_registry" "bench-container-registry" {
  name = var.acr_registry_name
  resource_group_name = var.resource_group_name
}