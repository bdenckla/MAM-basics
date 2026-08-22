# Viewing Image Metadata

To inspect embedded PNG tEXt chunks or other image metadata, use **XnView MP** (installed via winget as `XnSoft.XnViewMP`):

```powershell
Start-Process "C:\Program Files\XnViewMP\xnviewmp.exe" "path\to\image.png"
```

In XnView MP, press **Ctrl+I** (or **Edit → Metadata → Edit IPTC/XMP…**) to view properties including embedded text metadata.
