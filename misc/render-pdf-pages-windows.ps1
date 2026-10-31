# Render the pages of a PDF to PNG files with Windows' built-in PDF renderer, the Windows
# Runtime's Windows.Data.Pdf, so that an agent can read the pages as images without
# installing a PDF tool. Claude Code's Read tool, for one, reads a small PDF whole when it
# is not given pages, but given pages it renders them only through poppler's pdftoppm.
# dot-Codex/user-wide-AGENTS.md, "Shell, scripts, and file operations", sends agents here
# when pdftoppm is missing or they have no tool that shows a PDF's pages.
#
# Run it with Windows PowerShell 5.1, powershell.exe. PowerShell 7 cannot load the Windows
# Runtime types used below, so the script refuses to run there. From the root of a
# MAM-basics checkout:
#
#    powershell.exe -NoProfile -File misc/render-pdf-pages-windows.ps1 -PdfPath <pdf> -OutDir <directory>
#
# The script writes page-1.png, page-2.png and so on into OutDir, numbered by page,
# creating OutDir if it is absent and replacing files of the same names. It prints the
# page count and then each PNG's path and pixel size. -Pages takes the Read tool's
# syntax, such as 3 or 1-5, and renders only those pages. -Scale multiplies a page's size
# in device-independent pixels, 1/96 inch, so the default of 2 gives 192 pixels per inch
# whatever the display's scaling.
#
# Keep this file ASCII: Windows PowerShell 5.1 reads a script without a byte-order mark in
# the system's ANSI code page.

param(
    [Parameter(Mandatory)] [string] $PdfPath,
    [Parameter(Mandatory)] [string] $OutDir,
    [string] $Pages = '',
    [ValidateRange(0.1, 10.0)] [double] $Scale = 2.0
)

$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSEdition -ne 'Desktop') {
    throw 'Run this script with Windows PowerShell 5.1 (powershell.exe); PowerShell 7 cannot load the Windows Runtime types it uses.'
}
if (-not (Test-Path -LiteralPath $PdfPath -PathType Leaf)) {
    throw "No file at $PdfPath."
}
# The Windows Runtime's storage methods accept only absolute paths.
$pdfFullPath = (Get-Item -LiteralPath $PdfPath).FullName
$outFullPath = (New-Item -ItemType Directory -Force -Path $OutDir).FullName

# Naming each Windows Runtime type once, with its ContentType, makes PowerShell 5.1 load
# it, so that the bare type names below resolve.
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFolder, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
$null = [Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType = WindowsRuntime]
$null = [Windows.Data.Pdf.PdfPageRenderOptions, Windows.Data.Pdf, ContentType = WindowsRuntime]

# Windows Runtime methods are asynchronous. PowerShell cannot await them, so each one is
# converted to a .NET task by the matching AsTask extension method and waited on.
$asTaskMethods = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1
}
$asTaskForOperation = $asTaskMethods | Where-Object {
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
} | Select-Object -First 1
$asTaskForAction = $asTaskMethods | Where-Object {
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction'
} | Select-Object -First 1

function Wait-Operation($Operation, [type] $ResultType) {
    $task = $asTaskForOperation.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.Wait()
    $task.Result
}

function Wait-Action($Action) {
    $asTaskForAction.Invoke($null, @($Action)).Wait()
}

# Renders a page to the named PNG in OutDir, asking for its size in device-independent
# pixels times $Multiplier, and returns the PNG's path.
function Write-PagePng($Page, [string] $Name, [double] $Multiplier) {
    $options = New-Object Windows.Data.Pdf.PdfPageRenderOptions
    $options.DestinationWidth = [uint32] [Math]::Round($Page.Size.Width * $Multiplier)
    $options.DestinationHeight = [uint32] [Math]::Round($Page.Size.Height * $Multiplier)
    $collision = [Windows.Storage.CreationCollisionOption]::ReplaceExisting
    $file = Wait-Operation ($folder.CreateFileAsync($Name, $collision)) ([Windows.Storage.StorageFile])
    $access = [Windows.Storage.FileAccessMode]::ReadWrite
    $stream = Wait-Operation ($file.OpenAsync($access)) ([Windows.Storage.Streams.IRandomAccessStream])
    try {
        Wait-Action ($Page.RenderToStreamAsync($stream, $options))
    } finally {
        $stream.Dispose()
    }
    $file.Path
}

# Returns a PNG's width and height in pixels, which its IHDR chunk holds as big-endian
# 32-bit integers at byte offsets 16 and 20.
function Get-PngSize([string] $Path) {
    $reader = [IO.File]::OpenRead($Path)
    try {
        $header = New-Object byte[] 24
        if ($reader.Read($header, 0, 24) -ne 24) {
            throw "$Path is too short to be a PNG."
        }
    } finally {
        $reader.Dispose()
    }
    $width = [System.Net.IPAddress]::NetworkToHostOrder([BitConverter]::ToInt32($header, 16))
    $height = [System.Net.IPAddress]::NetworkToHostOrder([BitConverter]::ToInt32($header, 20))
    $width, $height
}

$pdfFile = Wait-Operation ([Windows.Storage.StorageFile]::GetFileFromPathAsync($pdfFullPath)) ([Windows.Storage.StorageFile])
$document = Wait-Operation ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($pdfFile)) ([Windows.Data.Pdf.PdfDocument])
$folder = Wait-Operation ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync($outFullPath)) ([Windows.Storage.StorageFolder])
$pageCount = [int] $document.PageCount

if ($Pages -eq '') {
    $firstPage = 1
    $lastPage = $pageCount
} elseif ($Pages -match '^\s*(\d+)\s*(-\s*(\d+)\s*)?$') {
    $firstPage = [int] $Matches[1]
    $lastPage = if ($Matches[3]) { [int] $Matches[3] } else { $firstPage }
} else {
    throw "-Pages takes one page or a range, such as 3 or 1-5, not '$Pages'."
}
if ($firstPage -lt 1 -or $lastPage -lt $firstPage -or $lastPage -gt $pageCount) {
    throw "-Pages $Pages is not a range within the PDF's $pageCount pages."
}

# Windows multiplies a requested size by the display's scaling, 2 at 200 percent. A trial
# rendering of the first page at its own size measures that multiplier, and every
# request below is divided by it. The trial's PNG is then overwritten.
$trialPage = $document.GetPage([uint32] ($firstPage - 1))
try {
    $trialPath = Write-PagePng $trialPage ('page-{0}.png' -f $firstPage) 1.0
    $displayScaling = (Get-PngSize $trialPath)[0] / [Math]::Round($trialPage.Size.Width)
} finally {
    $trialPage.Dispose()
}

'{0}: {1} pages' -f $pdfFullPath, $pageCount
for ($number = $firstPage; $number -le $lastPage; $number++) {
    $page = $document.GetPage([uint32] ($number - 1))
    try {
        $path = Write-PagePng $page ('page-{0}.png' -f $number) ($Scale / $displayScaling)
    } finally {
        $page.Dispose()
    }
    $width, $height = Get-PngSize $path
    '{0}: {1} x {2} px' -f $path, $width, $height
}
