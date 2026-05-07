param([string]$PayloadFile)

function Read-Payload {
    param([string]$Path)
    if ($Path) { return Get-Content -Raw -LiteralPath $Path }
    return [Console]::In.ReadToEnd()
}

$raw = Read-Payload -Path $PayloadFile
if (-not $raw) { exit 0 }

try {
    $json = $raw | ConvertFrom-Json -ErrorAction Stop
} catch {
    # best-effort: log raw
    $json = @{ raw = $raw }
}

$outDir = Join-Path -Path (Get-Location) -ChildPath 'artifacts'
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
"$((Get-Date).ToUniversalTime().ToString('o')) - POST_TOOL_USE - $($json | ConvertTo-Json -Depth 4)" | Out-File -FilePath (Join-Path $outDir 'post_tool_use.log') -Append -Encoding utf8

# Also append a structured audit line
$audit = @{ timestamp = (Get-Date).ToUniversalTime().ToString('o'); event = 'post_tool_use'; payload = $json }
$audit | ConvertTo-Json -Depth 5 | Out-File -FilePath (Join-Path $outDir 'audit.log') -Append -Encoding utf8

@{ status = 'logged' } | ConvertTo-Json -Depth 2
exit 0
