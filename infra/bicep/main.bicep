param location string = resourceGroup().location
param appName string
param storageName string
param keyVaultName string

resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

resource artifacts 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storage.name}/default/artifacts'
}
resource receipts 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storage.name}/default/receipts'
}
resource templates 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storage.name}/default/templates'
}

resource plan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${appName}-plan'
  location: location
  sku: { name: 'B1', tier: 'Basic' }
  kind: 'linux'
  properties: { reserved: true }
}

resource app 'Microsoft.Web/sites@2022-09-01' = {
  name: appName
  location: location
  kind: 'app,linux'
  identity: { type: 'SystemAssigned' }
  properties: {
    serverFarmId: plan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      appCommandLine: './startup.sh'
      appSettings: [
        { name: 'SCM_DO_BUILD_DURING_DEPLOYMENT', value: 'true' }
        { name: 'WEBSITES_PORT', value: '8000' }
        { name: 'AZURE_STORAGE_ACCOUNT_URL', value: 'https://${storage.name}.blob.core.windows.net' }
        { name: 'AZURE_STORAGE_CONTAINER_ARTIFACTS', value: 'artifacts' }
        { name: 'AZURE_STORAGE_CONTAINER_RECEIPTS', value: 'receipts' }
        { name: 'AZURE_STORAGE_CONTAINER_TEMPLATES', value: 'templates' }
        { name: 'AZURE_KEY_VAULT_URI', value: 'https://${keyVaultName}.vault.azure.net/' }
        { name: 'AZURE_KEY_VAULT_ENABLED', value: 'true' }
        { name: 'LOCAL_STORAGE_ENABLED', value: 'false' }
      ]
    }
  }
}
