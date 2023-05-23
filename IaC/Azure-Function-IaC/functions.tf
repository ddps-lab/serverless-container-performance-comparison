module "function" {
  count            = length(var.enabled_models)
  index_num        = count.index
  source           = "./function"
  resource_group   = data.azurerm_resource_group.bench-resource-group
  prefix           = var.prefix
  docker_registry = data.azurerm_container_registry.bench-container-registry
  model_name       = var.enabled_models[count.index]
  app_service_tier = var.model_resources[var.enabled_models[count.index]].tier
  app_service_size = var.model_resources[var.enabled_models[count.index]].size
  BlobStorageConnectionString = azurerm_storage_account.storage-account.primary_connection_string
}
