terraform {
  required_version = ">= 1.5"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
    time = {
      source  = "hashicorp/time"
      version = "~> 0.12"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

data "azurerm_client_config" "current" {}

# Storage and registry names must be globally unique, so add a random suffix
resource "random_string" "suffix" {
  length  = 5
  upper   = false
  special = false
}

locals {
  suffix = random_string.suffix.result
}

module "resource_group" {
  source   = "../../modules/resource-group"
  name     = "rg-${var.project}-${var.environment}"
  location = var.location
}

module "storage" {
  source              = "../../modules/storage-model-artifacts"
  name                = "st${var.project_short}${local.suffix}"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
}

module "registry" {
  source              = "../../modules/container-registry"
  name                = "acr${var.project_short}${local.suffix}"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
}

# Lets you (the logged-in user) upload the model with `az login` credentials
resource "azurerm_role_assignment" "me_blob_contributor" {
  scope                = module.storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

module "container_app" {
  source               = "../../modules/container-app"
  name                 = "ca-${var.project}-${var.environment}"
  resource_group_name  = module.resource_group.name
  location             = module.resource_group.location
  acr_id               = module.registry.id
  acr_login_server     = module.registry.login_server
  storage_account_id   = module.storage.id
  storage_account_name = module.storage.account_name
  image                = "${module.registry.login_server}/recommender-api:${var.image_tag}"
}

module "static_web_app" {
  source              = "../../modules/static-web-app"
  name                = "swa-${var.project}-${var.environment}"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
}