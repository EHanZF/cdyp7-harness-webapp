from app.core.config import settings

<<<<<<< HEAD

=======
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
def get_secret(name: str) -> str | None:
    if not settings.key_vault_enabled or not settings.key_vault_uri:
        return None
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
<<<<<<< HEAD

=======
>>>>>>> b0f8b70 (Add tooling API contract tests and validation output)
    client = SecretClient(vault_url=settings.key_vault_uri, credential=DefaultAzureCredential())
    return client.get_secret(name).value
