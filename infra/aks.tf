resource "azurerm_kubernetes_cluster" "main" {
  name                      = "aks-ai-factory-dev"
  location                  = azurerm_resource_group.main.location
  resource_group_name       = azurerm_resource_group.main.name
  dns_prefix                = "aiFactoryDev"
  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  default_node_pool {
    name                = "system"
    node_count          = 1
    vm_size             = "Standard_D2ps_v6"
    vnet_subnet_id      = azurerm_subnet.aks.id
    enable_auto_scaling = true
    min_count           = 1
    max_count           = 3
  }

  identity { type = "SystemAssigned" }
}
