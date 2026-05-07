param([string]$PayloadFile)

function Read-Payload {
    param([string]$Path)
    if ($Path) { return Get-Content -Raw -LiteralPath $Path }
    return [Console]::In.ReadToEnd()
}

$raw = Read-Payload -Path $PayloadFile
if (-not $raw) {
    Write-Error "no payload"
    exit 2
}

try {
    $json = $raw | ConvertFrom-Json -ErrorAction Stop
} catch {
    Write-Error "invalid json"
    exit 2
}

# Forbidden regexes (case-insensitive)
$patterns = @(
    '(?i)authorization:\s*bearer\s+',
    '(?i)api[_-]?key\s*=',
    '(?i)password\s*=',
    '(?i)client_secret\s*=',
    '(?i)private[_-]?key',
    '(?i)rm\s+-rf',
    '(?i)del\s+/s',
    '(?i)format\s+[a-z]:',
    '(?i)ssh\s+',
    '(?i)scp\s+',
    '(?i)curl\s+.*\|\s*(bash|sh|powershell)',
    '(?i)Invoke-Expression',
    '(?i)iex\s'
)

foreach ($p in $patterns) {
    if ($raw -match $p) {
        $out = @{ status = 'blocked'; reason = 'forbidden_pattern'; pattern = $p }
        $out | ConvertTo-Json -Depth 3
        exit 2
    }
}

# Require approval for ALM mutations or sensitive tool names
$approval_names = @('ALM_create','ALM_update','ALM_attach_file','Codebeamer_update','PTC_Windchill_update')
$name = $null
if ($json.params -and $json.params.name) { $name = $json.params.name }
if ($name -and ($approval_names -contains $name)) {
    $out = @{ status = 'approval_required'; reason = 'alm_mutation'; tool = $name }
    $out | ConvertTo-Json -Depth 3
    exit 3
}

@{ status = 'ok' } | ConvertTo-Json -Depth 3
exit 0
