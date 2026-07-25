param(
  [string]$OutputPath = (Join-Path $PSScriptRoot '..\dist\sketchup_agent_control.rbz'),
  [switch]$CreateRemoteSetupBundle
)

$source = (Resolve-Path (Join-Path $PSScriptRoot '..\src')).Path
$output = [System.IO.Path]::GetFullPath($OutputPath)
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $output) | Out-Null
if (Test-Path -LiteralPath $output) { Remove-Item -LiteralPath $output -Force }
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::Open($output, [System.IO.Compression.ZipArchiveMode]::Create)
try {
  Get-ChildItem -File -Recurse -LiteralPath $source | Where-Object { $_.Name -ne 'README.md' } | ForEach-Object {
    $entry = $_.FullName.Substring($source.Length + 1).Replace('\', '/')
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $entry) | Out-Null
  }
}
finally { $zip.Dispose() }
Write-Output $output

if ($CreateRemoteSetupBundle) {
  $repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
  $bundleRoot = Join-Path $repositoryRoot 'dist\remote-setup'
  $bundlePath = Join-Path $repositoryRoot 'dist\SketchUp-Agent-Control-Setup.zip'
  if (Test-Path -LiteralPath $bundleRoot) { Remove-Item -LiteralPath $bundleRoot -Recurse -Force }
  if (Test-Path -LiteralPath $bundlePath) { Remove-Item -LiteralPath $bundlePath -Force }
  New-Item -ItemType Directory -Force -Path (Join-Path $bundleRoot 'tools'), (Join-Path $bundleRoot 'scripts') | Out-Null
  Copy-Item -LiteralPath $output -Destination $bundleRoot
  Copy-Item -LiteralPath (Join-Path $repositoryRoot 'tools\bridge_core.py') -Destination (Join-Path $bundleRoot 'tools')
  Copy-Item -LiteralPath (Join-Path $repositoryRoot 'tools\bridge_cli.py') -Destination (Join-Path $bundleRoot 'tools')
  Copy-Item -LiteralPath (Join-Path $repositoryRoot 'tools\mcp_server.py') -Destination (Join-Path $bundleRoot 'tools')
  Copy-Item -LiteralPath (Join-Path $repositoryRoot 'scripts\setup_remote_computer.ps1') -Destination (Join-Path $bundleRoot 'scripts')
  Copy-Item -LiteralPath (Join-Path $repositoryRoot 'docs\remote-installation.md') -Destination (Join-Path $bundleRoot 'REMOTE-INSTALL.md')
  [System.IO.Compression.ZipFile]::CreateFromDirectory($bundleRoot, $bundlePath)
  Get-FileHash -Algorithm SHA256 -LiteralPath $bundlePath | ForEach-Object { "$($_.Hash)  $($_.Path)" } | Set-Content -Encoding ascii -NoNewline ("$bundlePath.sha256")
  Write-Output $bundlePath
}
