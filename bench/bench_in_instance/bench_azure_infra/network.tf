resource "azurerm_virtual_network" "bench-network" {
  name = "${var.prefix}-scpc-bench-network"
  location = data.azurerm_resource_group.bench-resource-group.location
  resource_group_name = data.azurerm_resource_group.bench-resource-group.name
  address_space = [ "192.168.0.0/16", "2001:db8::/48" ]
}

resource "azurerm_subnet" "bench-network-subnet" {
  name = "${var.prefix}-scpc-bench-network-subnet"
  virtual_network_name = azurerm_virtual_network.bench-network.name
  resource_group_name = data.azurerm_resource_group.bench-resource-group.name
  address_prefixes = [ "192.168.0.0/24", "2001:db8::/64" ] 
}