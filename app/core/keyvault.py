from app.core.config import settings


def get_secret(name: str) -> str | None:
    if not settings.key_vault_enabled or not settings.key_vault_uri:
        return None
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    client = SecretClient(vault_url=settings.key_vault_uri, credential=DefaultAzureCredential())
    return client.get_secret(name).value
