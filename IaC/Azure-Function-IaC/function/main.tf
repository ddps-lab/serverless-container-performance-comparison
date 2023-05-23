resource "azurerm_service_plan" "plan" {
  name                = "${var.prefix}${var.model_name}serviceplan"
  location            = var.resource_group.location
  resource_group_name = var.resource_group.name
  sku_name            = var.app_service_size
  os_type             = "Linux"
}

resource "azurerm_storage_account" "storage-account" {
  name                     = "${var.prefix}sa${var.index_num}"
  location                 = var.resource_group.location
  resource_group_name      = var.resource_group.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# resource "azurerm_user_assigned_identity" "azure_function_identity" {
#   location = var.resource_group.location
#   name = "${var.prefix}-scpc-${var.model_name}"
#   resource_group_name = var.resource_group.name
# }

# resource "azurerm_role_assignment" "azure_function_role_assign" {
#   scope = var.docker_registry.id
#   role_definition_name = "acrpull"
#   principal_id = azurerm_user_assigned_identity.azure_function_identity.principal_id
# }

resource "azurerm_linux_function_app" "azure_function" {
  name                       = "${replace(var.model_name, "_", "-")}-${var.prefix}"
  location                   = var.resource_group.location
  resource_group_name        = var.resource_group.name
  service_plan_id            = azurerm_service_plan.plan.id
  storage_account_name       = azurerm_storage_account.storage-account.name
  storage_account_access_key = azurerm_storage_account.storage-account.primary_access_key

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = false
    BlobStorageConnectionString = var.BlobStorageConnectionString
    BlobStorageContainerName = var.BlobStorageContainerName
  }

  site_config {
    application_stack {
      docker {
        registry_url      = var.docker_registry.login_server
        registry_username = var.docker_registry.admin_username
        registry_password = var.docker_registry.admin_password
        image_name        = "azure-function-${var.model_name}"
        image_tag         = "latest"
      }
    }

  }
}
