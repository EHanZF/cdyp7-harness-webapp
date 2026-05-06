terraform {
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.110" }
  }
}
provider "azurerm" { features {} }
variable "location" { default = "eastus" }
variable "resource_group_name" {}
variable "app_name" {}
variable "storage_account_name" {}
variable "key_vault_name" {}

resource "azurerm_resource_group" "rg" { name = var.resource_group_name location = var.location }
resource "azurerm_storage_account" "sa" {
  name = var.storage_account_name
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  account_tier = "Standard"
  account_replication_type = "LRS"
}
resource "azurerm_storage_container" "artifacts" { name = "artifacts" storage_account_name = azurerm_storage_account.sa.name container_access_type = "private" }
resource "azurerm_storage_container" "receipts" { name = "receipts" storage_account_name = azurerm_storage_account.sa.name container_access_type = "private" }
resource "azurerm_storage_container" "templates" { name = "templates" storage_account_name = azurerm_storage_account.sa.name container_access_type = "private" }
resource "azurerm_service_plan" "plan" { name = "${var.app_name}-plan" resource_group_name = azurerm_resource_group.rg.name location = azurerm_resource_group.rg.location os_type = "Linux" sku_name = "B1" }
resource "azurerm_linux_web_app" "app" {
  name = var.app_name
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  service_plan_id = azurerm_service_plan.plan.id
  identity { type = "SystemAssigned" }
  site_config { application_stack { python_version = "3.12" } app_command_line = "./startup.sh" }
  app_settings = {
    SCM_DO_BUILD_DURING_DEPLOYMENT = "true"
    WEBSITES_PORT = "8000"
    AZURE_STORAGE_ACCOUNT_URL = "https://${azurerm_storage_account.sa.name}.blob.core.windows.net"
    AZURE_STORAGE_CONTAINER_ARTIFACTS = "artifacts"
    AZURE_STORAGE_CONTAINER_RECEIPTS = "receipts"
    AZURE_STORAGE_CONTAINER_TEMPLATES = "templates"
    AZURE_KEY_VAULT_URI = "https://${var.key_vault_name}.vault.azure.net/"
    AZURE_KEY_VAULT_ENABLED = "true"
    LOCAL_STORAGE_ENABLED = "false"
  }
}
