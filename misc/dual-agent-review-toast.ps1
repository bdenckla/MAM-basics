param([Parameter(Mandatory)][string]$MessageFile)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null
$reviewApp = @(Get-StartApps -Name 'Windows PowerShell' | Where-Object Name -eq 'Windows PowerShell')
if ($reviewApp.Count -ne 1) {
    throw 'Expected one installed Windows PowerShell notification identity.'
}
$reviewAppId = $reviewApp[0].AppID
$reviewNotifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($reviewAppId)
if ($reviewNotifier.Setting.ToString() -ne 'Enabled') {
    throw "Windows blocks relay notifications: $($reviewNotifier.Setting). Check Windows PowerShell in Settings > System > Notifications."
}
$reviewMessage = [System.IO.File]::ReadAllText($MessageFile, [System.Text.Encoding]::UTF8)
$reviewXml = New-Object Windows.Data.Xml.Dom.XmlDocument
$reviewXml.LoadXml('<toast><visual><binding template="ToastGeneric"><text>Dual-agent review</text><text></text></binding></visual></toast>')
$reviewXml.GetElementsByTagName('text').Item(1).InnerText = $reviewMessage
$reviewToast = [Windows.UI.Notifications.ToastNotification]::new($reviewXml)
$reviewToast.Tag = [Guid]::NewGuid().ToString('N').Substring(0, 16)
$reviewToast.Group = 'dualagentreview'
$reviewNotifier.Show($reviewToast)
$reviewHistory = [Windows.UI.Notifications.ToastNotificationManager]::History.GetHistory($reviewAppId)
[ordered]@{
    senderName = $reviewApp[0].Name
    senderId = $reviewAppId
    setting = $reviewNotifier.Setting.ToString()
    submitted = $true
    tag = $reviewToast.Tag
    group = $reviewToast.Group
    recordedInHistory = [bool]@($reviewHistory | Where-Object { $_.Tag -eq $reviewToast.Tag -and $_.Group -eq $reviewToast.Group }).Count
} | ConvertTo-Json
