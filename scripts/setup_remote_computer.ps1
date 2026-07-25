[CmdletBinding(SupportsShouldProcess)]
param(
  [string]$BridgeRoot = (Join-Path $env:LOCALAPPDATA 'Beautiful Insights\SketchUp Agent Control'),
  [switch]$SkipPythonCheck
)

$ErrorActionPreference = 'Stop'
$directories = 'inbox', 'processing', 'outbox', 'errors', 'snapshots', 'exports', 'backups', 'logs'

if (-not $SkipPythonCheck) {
  $python = Get-Command python -ErrorAction SilentlyContinue
  if (-not $python) {
    throw 'Python 3.11 or later is required. Install it from python.org, open a new PowerShell window, then rerun this setup script.'
  }
  $version = & $python.Source --version 2>&1
  if ($LASTEXITCODE -ne 0) { throw "Unable to run Python: $version" }
  Write-Host "Found $version"
}

if ($PSCmdlet.ShouldProcess($BridgeRoot, 'Create local bridge folders')) {
  New-Item -ItemType Directory -Force -Path $BridgeRoot | Out-Null
  foreach ($directory in $directories) {
    New-Item -ItemType Directory -Force -Path (Join-Path $BridgeRoot $directory) | Out-Null
  }
}

Write-Host "Bridge root: $BridgeRoot"
Write-Host 'Next: install sketchup_agent_control.rbz through SketchUp Extension Manager, open a blank model, then run:'
Write-Host '  python .\tools\bridge_cli.py status --timeout 30'
