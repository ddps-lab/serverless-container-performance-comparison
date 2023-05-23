output "blob_connection_string" {
  value = nonsensitive(azurerm_storage_account.storage-account.primary_connection_string)
}

output "blob_container_name" {
  value = azurerm_storage_container.storage-container.name
}