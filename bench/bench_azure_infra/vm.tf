resource "azurerm_network_security_group" "bench-vm-sg" {
  name                = "${var.prefix}-bench-vm-sg"
  location            = data.azurerm_resource_group.bench-resource-group.location
  resource_group_name = data.azurerm_resource_group.bench-resource-group.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_public_ip" "bench-vm-public-ipv4" {
  name                = "${var.prefix}-scpc-bench-vm-public-ipv4"
  location            = data.azurerm_resource_group.bench-resource-group.location
  resource_group_name = data.azurerm_resource_group.bench-resource-group.name
  allocation_method   = "Dynamic"
  ip_version          = "IPv4"
}

resource "azurerm_network_interface" "bench-vm-nic" {
  name                = "${var.prefix}-scpc-bench-vm-nic"
  location            = data.azurerm_resource_group.bench-resource-group.location
  resource_group_name = data.azurerm_resource_group.bench-resource-group.name
  enable_accelerated_networking = true
  ip_configuration {
    primary                       = true
    name                          = "${var.prefix}-scpc-bench-vm-nic-ipv4"
    subnet_id                     = azurerm_subnet.bench-network-subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.bench-vm-public-ipv4.id
    private_ip_address_version    = "IPv4"
  }

  ip_configuration {
    name                          = "${var.prefix}-scpc-bench-vm-nic-ipv6"
    subnet_id                     = azurerm_subnet.bench-network-subnet.id
    private_ip_address_allocation = "Dynamic"
    private_ip_address_version    = "IPv6"
  }
}

resource "azurerm_network_interface_security_group_association" "bench-nic-sg-association" {
  network_interface_id      = azurerm_network_interface.bench-vm-nic.id
  network_security_group_id = azurerm_network_security_group.bench-vm-sg.id
}

resource "azurerm_linux_virtual_machine" "bench-vm" {
  name                  = "${var.prefix}-scpc-bench-vm"
  resource_group_name   = data.azurerm_resource_group.bench-resource-group.name
  location              = data.azurerm_resource_group.bench-resource-group.location
  size                  = "Standard_D2s_v3"
  admin_username        = var.ssh-username
  network_interface_ids = [azurerm_network_interface.bench-vm-nic.id]
  admin_ssh_key {
    username   = var.ssh-username
    public_key = data.azurerm_ssh_public_key.ssh-key.public_key
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 64
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }
}
