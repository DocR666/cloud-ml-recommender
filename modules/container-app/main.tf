variable "name" { type = string }
variable "resource_group_name" { type = string }
variable "location" { type = string }
variable "acr_id" { type = string }
variable "acr_login_server" { type = string }
variable "storage_account_id" { type = string }
variable "storage_account_name" { type = string }
variable "image" { type = string }

resource "azurerm_log_analytics_workspace" "this" {
  name                = "log-${var.name}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "this" {
  name                       = "cae-${var.name}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.this.id
}

# The app's own identity: no passwords or keys anywhere
resource "azurerm_user_assigned_identity" "app" {
  name                = "id-${var.name}"
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = var.acr_id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

resource "azurerm_role_assignment" "blob_reader" {
  scope                = var.storage_account_id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

# Role assignments take a little while to take effect
resource "time_sleep" "role_propagation" {
  depends_on      = [azurerm_role_assignment.acr_pull, azurerm_role_assignment.blob_reader]
  create_duration = "90s"
}

resource "azurerm_container_app" "this" {
  name                         = var.name
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }

  registry {
    server   = var.acr_login_server
    identity = azurerm_user_assigned_identity.app.id
  }

  template {
    min_replicas = 0 # scales to zero when idle; set to 1 on demo day to avoid a cold start
    max_replicas = 1

    container {
      name   = "api"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "STORAGE_ACCOUNT_NAME"
        value = var.storage_account_name
      }
      env {
        name  = "MODEL_CONTAINER"
        value = "models"
      }
      env {
        name  = "AZURE_CLIENT_ID"
        value = azurerm_user_assigned_identity.app.client_id
      }
    }
  }

  lifecycle {
    ignore_changes = [template[0].container[0].image]
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  depends_on = [time_sleep.role_propagation]
}

output "url" {
  value = "https://${azurerm_container_app.this.ingress[0].fqdn}"
}