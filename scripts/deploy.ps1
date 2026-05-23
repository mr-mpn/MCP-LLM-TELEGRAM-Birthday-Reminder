# Full build and deploy script for Birthday Bot

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$DistDir = Join-Path $ProjectRoot "dist"
$TerraformDir = Join-Path $ProjectRoot "terraform"

Write-Host "=== Birthday Bot - Build & Deploy ===" -ForegroundColor Cyan
Write-Host ""

# --- Clean ---
Write-Host "[1/4] Cleaning dist..." -ForegroundColor Yellow
if (Test-Path $DistDir) { Remove-Item -Recurse -Force $DistDir }
New-Item -ItemType Directory -Path $DistDir | Out-Null

# --- Build dependencies layer (Linux x86_64, Python 3.12) ---
Write-Host "[2/4] Building dependencies layer (Linux/Python 3.12)..." -ForegroundColor Yellow
$LayerDir = Join-Path $DistDir "layer\python"
New-Item -ItemType Directory -Path $LayerDir -Force | Out-Null

pip install -r (Join-Path $ProjectRoot "requirements.txt") -t $LayerDir --platform manylinux2014_x86_64 --python-version 3.12 --only-binary=:all: --implementation cp --quiet

Compress-Archive -Path (Join-Path $DistDir "layer\python") -DestinationPath (Join-Path $DistDir "dependencies_layer.zip")
Remove-Item -Recurse -Force (Join-Path $DistDir "layer")
Write-Host "  -> dist/dependencies_layer.zip" -ForegroundColor Green

# --- Build Lambda code package ---
Write-Host "[3/4] Building Lambda code package..." -ForegroundColor Yellow
Compress-Archive -Path (Join-Path $ProjectRoot "src\*") -DestinationPath (Join-Path $DistDir "chat_lambda.zip")
Write-Host "  -> dist/chat_lambda.zip" -ForegroundColor Green

# --- Terraform deploy ---
Write-Host "[4/4] Deploying with Terraform..." -ForegroundColor Yellow
Push-Location $TerraformDir

terraform init -input=false -no-color 2>&1 | Out-Null
terraform taint aws_lambda_layer_version.dependencies 2>&1 | Out-Null
terraform apply -auto-approve -input=false

Pop-Location

Write-Host ""
Write-Host "=== Deploy complete! ===" -ForegroundColor Green
