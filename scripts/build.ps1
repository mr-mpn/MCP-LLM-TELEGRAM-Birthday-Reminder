# Build script for packaging Lambda functions and dependencies layer (Windows)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$DistDir = Join-Path $ProjectRoot "dist"

Write-Host "=== Building Birthday Bot Lambda Package ==="

# Clean dist directory
if (Test-Path $DistDir) { Remove-Item -Recurse -Force $DistDir }
New-Item -ItemType Directory -Path $DistDir | Out-Null

# --- Build dependencies layer ---
Write-Host "Building dependencies layer..."
$LayerDir = Join-Path $DistDir "layer\python"
New-Item -ItemType Directory -Path $LayerDir -Force | Out-Null

pip install -r (Join-Path $ProjectRoot "requirements.txt") -t $LayerDir --quiet

Compress-Archive -Path (Join-Path $DistDir "layer\python") -DestinationPath (Join-Path $DistDir "dependencies_layer.zip")
Remove-Item -Recurse -Force (Join-Path $DistDir "layer")

Write-Host "Dependencies layer built: dist/dependencies_layer.zip"

# --- Build Lambda code package ---
Write-Host "Building Lambda code package..."
Compress-Archive -Path (Join-Path $ProjectRoot "src\*") -DestinationPath (Join-Path $DistDir "chat_lambda.zip")

Write-Host "Lambda code built: dist/chat_lambda.zip"
Write-Host ""
Write-Host "=== Build complete! ==="
Write-Host "Next steps:"
Write-Host "  1. cd terraform"
Write-Host "  2. terraform init"
Write-Host "  3. terraform plan"
Write-Host "  4. terraform apply"
