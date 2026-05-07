param([string]$PayloadFile)

try {
    $correlation = [guid]::NewGuid().ToString()
    $envName = $env:ENV
    if ($envName -eq 'production') {
        if (-not $env:AZURE_STORAGE_ACCOUNT_URL) {
            Write-Error "Missing required AZURE_STORAGE_ACCOUNT_URL in production environment"
            exit 2
        }
    }

    $context = @{
        correlation_id = $correlation
        event = 'SessionStart'
        timestamp = (Get-Date).ToUniversalTime().ToString('o')
        env = @{ ENV = $envName; AZURE_STORAGE_ACCOUNT_URL = $env:AZURE_STORAGE_ACCOUNT_URL }
    }

    $outDir = Join-Path -Path (Get-Location) -ChildPath 'artifacts'
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    $path = Join-Path $outDir "$($correlation)-session.json"
    $context | ConvertTo-Json -Depth 5 | Out-File -FilePath $path -Encoding utf8
    $context | ConvertTo-Json -Depth 5
    exit 0
} catch {
    Write-Error "session_start_hook_failed: $_"
    exit 3
}
