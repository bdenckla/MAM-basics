# Opening HTML Files

When displaying an HTML file that only uses local/relative resources (images, CSS, etc.), open it directly as a file (`Start-Process "path/to/file.html"`) rather than starting a local HTTP server. Only use a server when the page requires it (e.g., fetching from external APIs with CORS restrictions, or serving content that browsers block via `file://`).

**Fragment anchors (`#id`):** `file:///` URIs with `#fragment` do NOT reliably scroll to the anchor — the browser drops the fragment. Use a local HTTP server instead:

```powershell
# Start server (background):
python -m http.server 8471 --directory gh-pages

# Open anchored URLs:
$sids = @("SID1","SID2","SID3")
foreach ($s in $sids) { Start-Process "http://localhost:8471/jobn/job1_full_list_details.html#row-$s"; Start-Sleep -Milliseconds 500 }
```

The 500 ms delay prevents tabs from being dropped.

**Browser caching:** When verifying updated images served via localhost, the browser may show stale cached versions. Use Edge in InPrivate mode to guarantee a fresh load:

```powershell
Start-Process "msedge" "--inprivate http://localhost:8471/jobn/job1_full_list_details.html#row-SID"
```
