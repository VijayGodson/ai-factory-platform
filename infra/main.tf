terraform {
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.100" }
    random  = { source = "hashicorp/random" }
  }
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "sttfstate613"
    container_name       = "tfstate"
    key                  = "ai-factory.tfstate"
  }
}
provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}
resource "random_string" "suffix" {
  length  = 5
  special = false
  upper   = false
}
