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

resource "azurerm_storage_account" "storage-account" {
  name                     = "${var.prefix}scpcblobsa"
  location                 = data.azurerm_resource_group.bench-resource-group.location
  resource_group_name      = data.azurerm_resource_group.bench-resource-group.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "storage-container" {
  name = "${var.prefix}scpcstoragecontainer"
  storage_account_name = azurerm_storage_account.storage-account.name
  container_access_type = "private"
}
