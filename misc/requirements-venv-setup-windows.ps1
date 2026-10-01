# Misc. software to install:
#
#    Python 3.13 (python.org installer, NOT the Microsoft Store)
#    Git (web page download)
#    GitHub Desktop (web page download) or SmartGit
#    Visual Studio Code (web page download)
#    Windows Terminal (Microsoft Store) or Windows Terminal Preview (Microsoft Store)
#    More recent PowerShell? (Microsoft Store)
#
#  (GitHub Desktop is because I can't get remote access, e.g. clone & push, working from within Visual Studio Code.)
#
#
# To allow execution of this and other PowerShell scripts:
#
#    Set-ExecutionPolicy RemoteSigned
#
# Run this script with the repo root as the current directory, e.g.
#
#    ./misc/requirements-venv-setup-windows.ps1

param([string]$BasePython = 'python')

$ErrorActionPreference = 'Stop'
$RepositoryRoot = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path -LiteralPath "$RepositoryRoot/.git" -PathType Container)) {
    throw 'Setup requires a full clone; a linked worktree uses its home clone environment.'
}
foreach ($InputName in @('requirements.txt', 'constraints.txt')) {
    if (-not (Test-Path -LiteralPath "$RepositoryRoot/$InputName" -PathType Leaf)) {
        throw "The tracked $InputName is required before environment setup."
    }
}
$EnvironmentRoot = "$RepositoryRoot/.venv"
$EnvironmentItem = $null
try {
    $EnvironmentItem = Get-Item -LiteralPath $EnvironmentRoot -Force
} catch [System.Management.Automation.ItemNotFoundException] {
    # Create only when the environment path is absent.
}
if ($null -ne $EnvironmentItem) {
    if ($EnvironmentItem.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw 'The environment must be a real directory, never a link or junction.'
    }
    if (-not $EnvironmentItem.PSIsContainer) {
        throw 'The existing environment path must be a directory.'
    }
} else {
    & $BasePython -m venv $EnvironmentRoot
    if ($LASTEXITCODE -ne 0) {
        throw 'Environment creation failed.'
    }
}
$EnvironmentPython = "$EnvironmentRoot/Scripts/python.exe"
if (-not (Test-Path -LiteralPath $EnvironmentPython -PathType Leaf) -or
    -not (Test-Path -LiteralPath "$EnvironmentRoot/pyvenv.cfg" -PathType Leaf)) {
    throw 'The existing environment is incomplete; repair it deliberately.'
}
& $EnvironmentPython -m pip install --no-input -r "$RepositoryRoot/requirements.txt" -c "$RepositoryRoot/constraints.txt"
if ($LASTEXITCODE -ne 0) {
    throw 'Constrained dependency installation failed.'
}
& $EnvironmentPython -m pip check
if ($LASTEXITCODE -ne 0) {
    throw 'Installed dependencies do not satisfy pip check.'
}
