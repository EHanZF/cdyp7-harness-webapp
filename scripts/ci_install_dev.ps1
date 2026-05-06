param(
    [string]$RequirementsDev = "requirements-dev.txt"
)

Write-Host "Checking for dev requirements file: $RequirementsDev"
if (Test-Path $RequirementsDev) {
    Write-Host "Installing dev requirements from $RequirementsDev"
    python -m pip install -r $RequirementsDev
} else {
    Write-Host "No dev requirements file found at $RequirementsDev — skipping."
}
