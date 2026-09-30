param([Parameter(Mandatory)][string]$MessageFile)
$ErrorActionPreference = 'Stop'
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null
$reviewMessage = [System.IO.File]::ReadAllText($MessageFile, [System.Text.Encoding]::UTF8)
$reviewXml = New-Object Windows.Data.Xml.Dom.XmlDocument
$reviewXml.LoadXml('<toast><visual><binding template="ToastGeneric"><text>Dual-agent review</text><text></text></binding></visual></toast>')
$reviewXml.GetElementsByTagName('text').Item(1).InnerText = $reviewMessage
$reviewToast = [Windows.UI.Notifications.ToastNotification]::new($reviewXml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Microsoft.Windows.PowerShell').Show($reviewToast)
