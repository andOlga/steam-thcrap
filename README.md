![](https://repository-images.githubusercontent.com/580734620/d3bdc5b8-36ee-4b32-b35c-a6bf8c29074c)

# steam-thcrap
This is a small program to automatically add [thcrap](https://thpatch.net)-patched [Touhou](https://touhou-project.news) games to [Steam](https://s.team) as shortcuts ("Non-Steam Games").
It was created due to the fact that adding them manually these days can take a damn hour or so since there's tons of games and Steam's built-in shortcut editor is wildly inefficient for adding multiple games with custom launch arguments.

## Usage instructions
[Download](../../releases/latest/download/steam-thcrap.zip) the latest release, extract and place the `steam-thcrap` folder near `thcrap.exe`, and run the `steam-thcrap.exe` file inside. You are done.

On Linux? Use [this](https://github.com/tactikauan/thcrap-steam-proton-wrapper) instead.

## Build instructions (for developers only)
(in a [Git Bash](https://git-scm.com) shell, with [Python](https://python.org), [NanaZip](https://github.com/M2Team/NanaZip) and [GitHub CLI](https://cli.github.com) installed)

```bash
python -mvenv venv
source venv/Scripts/activate
pip install -r requirements.txt
# ... make and test your changes...
black steam-thcrap.py
pyinstaller --icon icon.ico steam-thcrap.py
cp -r grid dist/steam-thcrap/
cd dist
7z a steam-thcrap.zip steam-thcrap
gh release create vX.X.X steam-thcrap.zip
```
