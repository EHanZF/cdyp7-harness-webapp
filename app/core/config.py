from pathlib import Path
import json, os, yaml

ROOT = Path(__file__).resolve().parents[2]

def load_adapter(path: str | None = None) -> dict:
    p = Path(path) if path else ROOT / 'config' / 'runtime-adapter.yaml'
    return yaml.safe_load(p.read_text(encoding='utf-8'))

def assert_adapter(adapter: dict) -> None:
    tools = adapter['tools']
    if tools['namespace'] != 'harness' or tools['mode'] != 'strict' or tools['on_violation'] != 'fail_closed':
        raise RuntimeError('BOOT_DENY: harness tool namespace must be strict/fail_closed')
    expected = ['harness.generate_release_sheet','harness.validate_release_sheet','harness.write_receipt','harness.fetch_artifact','harness.resolve_replay']
    if tools['exposed'] != expected:
        raise RuntimeError('BOOT_DENY: exposed tooling surface mismatch')
    gen = adapter.get('release_sheet_generator', {})
    for key in ['approve_release','infer_missing_values','sign_for_approvers','commit_directly_to_repository','bypass_hitl','mutate_source_systems']:
        if gen.get(key) is not False:
            raise RuntimeError(f'BOOT_DENY: release generator boundary violation: {key}')
    if adapter['replay']['rerun_retrieval'] is not False or adapter['replay']['require_cache_hit'] is not True:
        raise RuntimeError('BOOT_DENY: replay must be deterministic and fail-closed')

class Settings:
    storage_account_url: str | None = os.getenv('AZURE_STORAGE_ACCOUNT_URL')
    artifacts_container: str = os.getenv('AZURE_STORAGE_CONTAINER_ARTIFACTS', 'artifacts')
    receipts_container: str = os.getenv('AZURE_STORAGE_CONTAINER_RECEIPTS', 'receipts')
    templates_container: str = os.getenv('AZURE_STORAGE_CONTAINER_TEMPLATES', 'templates')
    key_vault_uri: str | None = os.getenv('AZURE_KEY_VAULT_URI')
    key_vault_enabled: bool = os.getenv('AZURE_KEY_VAULT_ENABLED', 'false').lower() == 'true'
    local_storage_enabled: bool = os.getenv('LOCAL_STORAGE_ENABLED', 'true').lower() == 'true'

settings = Settings()
