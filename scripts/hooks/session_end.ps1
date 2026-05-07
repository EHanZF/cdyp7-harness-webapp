param([string]$SessionFile)

try {
    $outDir = Join-Path -Path (Get-Location) -ChildPath 'artifacts'
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    if ($SessionFile -and (Test-Path $SessionFile)) {
        $session = Get-Content -Raw -LiteralPath $SessionFile | ConvertFrom-Json
    } else {
        # find latest session file
        $files = Get-ChildItem -Path $outDir -Filter '*-session.json' | Sort-Object LastWriteTime -Descending
        if ($files.Count -gt 0) { $session = Get-Content -Raw -LiteralPath $files[0].FullName | ConvertFrom-Json }
        else { $session = @{ correlation_id = 'unknown'; note = 'no_session_found' } }
    }

    $summary = @{ event = 'SessionEnd'; correlation_id = $session.correlation_id; timestamp = (Get-Date).ToUniversalTime().ToString('o') }
    $path = Join-Path $outDir "$($session.correlation_id)-summary.json"
    $summary | ConvertTo-Json -Depth 5 | Out-File -FilePath $path -Encoding utf8
    $summary | ConvertTo-Json -Depth 5
    exit 0
} catch {
    Write-Error "session_end_hook_failed: $_"
    exit 3
}
