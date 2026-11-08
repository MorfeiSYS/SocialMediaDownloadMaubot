#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoDir = Resolve-Path (Join-Path $scriptDir '..')
$versionScript = Join-Path $scriptDir 'release_version.py'

$pythonBin = if ($env:PYTHON) { $env:PYTHON } else { 'python' }

$noBump = $false
$outputPath = $null
foreach ($arg in $args) {
    if ($arg -eq '--no-bump') {
        $noBump = $true
    }
    elseif ($null -eq $outputPath) {
        $outputPath = $arg
    }
}

if ($noBump) {
    $version = & $pythonBin $versionScript current
}
else {
    $version = & $pythonBin $versionScript bump
}
if ($LASTEXITCODE -ne 0) { throw "release_version.py failed" }
$version = $version.Trim()

if (-not $outputPath) {
    $outputPath = Join-Path $repoDir "build\SocialMediaDown-v$version.mbp"
}

if (-not [System.IO.Path]::IsPathRooted($outputPath)) {
    $outputPath = Join-Path (Get-Location) $outputPath
}
$outputPath = [System.IO.Path]::GetFullPath($outputPath)

$buildDir = Join-Path ([System.IO.Path]::GetTempPath()) ("socialmediadownload-build.{0}" -f [guid]::NewGuid().ToString('N'))
$payloadDir = Join-Path $buildDir 'payload'

try {
    New-Item -ItemType Directory -Path $payloadDir -Force | Out-Null
    New-Item -ItemType Directory -Path (Split-Path $outputPath -Parent) -Force | Out-Null

    & $pythonBin -m pip install `
        --disable-pip-version-check `
        --no-compile `
        --no-deps `
        --requirement (Join-Path $repoDir 'requirements.txt') `
        --target $payloadDir
    if ($LASTEXITCODE -ne 0) { throw "pip install failed with exit code $LASTEXITCODE" }

    $binDir = Join-Path $payloadDir 'bin'
    if (Test-Path $binDir) {
        Remove-Item -LiteralPath $binDir -Recurse -Force
    }

    Copy-Item (Join-Path $repoDir 'base-config.yaml') $payloadDir
    Copy-Item (Join-Path $repoDir 'maubot.yaml') $payloadDir
    Copy-Item (Join-Path $repoDir 'socialmediadownload.py') $payloadDir

    $stagingMbp = Join-Path $buildDir 'package.mbp'
    & $pythonBin (Join-Path $scriptDir 'package_mbp.py') $payloadDir $stagingMbp
    if ($LASTEXITCODE -ne 0) { throw "package_mbp.py failed" }

    Move-Item -LiteralPath $stagingMbp -Destination $outputPath -Force

    & $pythonBin (Join-Path $scriptDir 'verify-mbp.py') $outputPath
    if ($LASTEXITCODE -ne 0) { throw "verify-mbp.py failed" }
    Write-Host "Built $outputPath (version $version)"
}
finally {
    if (Test-Path $buildDir) {
        Remove-Item -LiteralPath $buildDir -Recurse -Force
    }
}
