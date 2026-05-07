try {
    $python = Join-Path -Path (Get-Location) -ChildPath '.venv\Scripts\python.exe'
    if (-not (Test-Path $python)) { $python = 'python' }

    Write-Output 'Running unit tests...'
    & $python -m pytest -q
    $rc = $LASTEXITCODE
    if ($rc -ne 0) {
        Write-Error "tests_failed"
        exit $rc
    }

    Write-Output 'Running pylint (if available)...'
    & $python -m pylint --disable=C,R,W app tests
    $rc = $LASTEXITCODE
    if ($rc -ne 0) {
        Write-Warning 'pylint reported issues; continuing but please review.'
    }

    Write-Output 'pre-push validation passed.'
    exit 0
} catch {
    Write-Error "pre_push_validate_failed: $_"
    exit 2
}
