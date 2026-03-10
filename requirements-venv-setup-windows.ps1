# Misc. software to install:
#
#    Python (Microsoft Store)
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
# Run this script with 'py' as the current directory, e.g.
#
#    PS C:\Users\BenDe\GitRepos\MAM-basics\py> .\requirements-venv-setup-windows.ps1

python -m venv venv
if (-not $?)
{
    throw 'python -m venv venv failed'
}

venv\Scripts\Activate.ps1
if (-not $?)
{
    throw 'venv\scripts\activate.ps1 failed'
}

pip install -r requirements.txt
if (-not $?)
{
    throw 'pip install -r requirements.txt failed'
}
