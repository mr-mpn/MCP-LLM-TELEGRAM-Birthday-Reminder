# Full build and deploy script for Birthday Bot

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$DistDir = Join-Path $ProjectRoot "dist"
$TerraformDir = Join-Path $ProjectRoot "terraform"

Add-Type -AssemblyName System.IO.Compression.FileSystem

function Create-ZipFromDirectory($sourceDir, $zipPath) {
    if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
    [System.IO.Compression.ZipFile]::CreateFromDirectory($sourceDir, $zipPath)
}

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

# Wait for file handles to release
Start-Sleep -Seconds 2

Create-ZipFromDirectory (Join-Path $DistDir "layer") (Join-Path $DistDir "dependencies_layer.zip")
Remove-Item -Recurse -Force (Join-Path $DistDir "layer")
Write-Host "  -> dist/dependencies_layer.zip" -ForegroundColor Green

# --- Build Lambda code package ---
Write-Host "[3/4] Building Lambda code package..." -ForegroundColor Yellow
Create-ZipFromDirectory (Join-Path $ProjectRoot "src") (Join-Path $DistDir "chat_lambda.zip")
Write-Host "  -> dist/chat_lambda.zip" -ForegroundColor Green

# --- Terraform deploy ---
Write-Host "[4/4] Deploying with Terraform..." -ForegroundColor Yellow
Push-Location $TerraformDir

terraform init -input=false -no-color 2>&1 | Out-Null
terraform apply -auto-approve -input=false -replace="aws_lambda_layer_version.dependencies"

Pop-Location

Write-Host ""
Write-Host "=== Deploy complete! ===" -ForegroundColor Green
