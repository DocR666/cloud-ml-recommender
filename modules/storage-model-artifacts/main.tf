variable "name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }

resource "azurerm_storage_account" "this" {
  name                            = var.name
  resource_group_name             = var.resource_group_name
  location                        = var.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
}

resource "azurerm_storage_container" "models" {
  name                  = "models"
  storage_account_name  = azurerm_storage_account.this.name
  container_access_type = "private"
}

output "id" { value = azurerm_storage_account.this.id }
output "account_name" { value = azurerm_storage_account.this.name }
output "container_name" { value = azurerm_storage_container.models.name }