# Azure Deployment

Use `azure-pipelines.yml` for Azure DevOps. The app deploys to Azure App Service Linux Python 3.12 with Oryx build.

## Blob Storage

```text
artifacts container: DOCX artifacts
receipts container: immutable receipt JSON
```

## Key Vault

Set:

```text
AZURE_KEY_VAULT_URI
AZURE_KEY_VAULT_ENABLED=true
```

The code includes `app/core/keyvault.py` for secret retrieval using Managed Identity.
