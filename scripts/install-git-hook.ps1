# Instala prepare-commit-msg em .git/hooks/ (remove co-autoria Cursor).
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$gitDir = Join-Path $repoRoot ".git"

if (-not (Test-Path $gitDir)) {
    Write-Error "Repositorio Git nao encontrado em: $repoRoot`nExecute 'git init' antes de instalar o hook."
}

$hooksDir = Join-Path $gitDir "hooks"
$source = Join-Path $PSScriptRoot "prepare-commit-msg"
$target = Join-Path $hooksDir "prepare-commit-msg"

if (-not (Test-Path $source)) {
    Write-Error "Script fonte nao encontrado: $source"
}

New-Item -ItemType Directory -Force -Path $hooksDir | Out-Null
Copy-Item -Path $source -Destination $target -Force

Write-Host "Hook instalado: $target"
