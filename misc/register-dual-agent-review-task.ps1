param([Parameter(Mandatory)][string]$Repository)
$ErrorActionPreference = 'Stop'
$reviewRoot = (Resolve-Path -LiteralPath $Repository).Path
$reviewPython = Join-Path $reviewRoot '.venv/Scripts/pythonw.exe'
$reviewEntry = Join-Path $reviewRoot 'py/main_repo_util.py'
if (-not (Test-Path -LiteralPath $reviewPython) -or -not (Test-Path -LiteralPath $reviewEntry)) {
    throw 'The exact helper clone must contain its own pythonw.exe and main_repo_util.py.'
}
$reviewAction = New-ScheduledTaskAction -Execute $reviewPython -Argument ('"' + $reviewEntry + '" --dual-agent-review tick') -WorkingDirectory $reviewRoot
$reviewConfiguration = Get-Content -LiteralPath (Join-Path $reviewRoot 'in/dual_agent_review_automation.json') -Raw | ConvertFrom-Json
if (-not $reviewConfiguration.production_enabled) {
    throw 'Production rollout is disabled pending protocol approval and live rehearsal.'
}
$reviewTrigger = New-ScheduledTaskTrigger -Once -At ([DateTime]::Now.AddMinutes(1)) -RepetitionInterval (New-TimeSpan -Minutes $reviewConfiguration.tick_interval_minutes)
$reviewPrincipal = New-ScheduledTaskPrincipal -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited
$reviewSettings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit ([TimeSpan]::Zero)
Register-ScheduledTask -TaskName 'Dual-agent review relay' -Action $reviewAction -Trigger $reviewTrigger -Principal $reviewPrincipal -Settings $reviewSettings -Description ('Registered automated rounds from ' + $reviewRoot) -ErrorAction Stop
