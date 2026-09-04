$repo_root = (Get-Item "$PSScriptRoot/../..").FullName
$product_command = "$repo_root/py/main_diffable_pointed_hebrew.py"
$python = "$repo_root/.venv/Scripts/python.exe"

& $python $product_command "$PSScriptRoot/zarqa-table-from-hebrew-wikisource.txt" "$PSScriptRoot/zarqa-table-from-hebrew-wikisource.dph.txt"
& $python $product_command "$PSScriptRoot/zarqa-table-from-open-siddur-project.txt" "$PSScriptRoot/zarqa-table-from-open-siddur-project.dph.txt"
