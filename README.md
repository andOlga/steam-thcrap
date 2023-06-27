This project is no longer maintained.

Steam's internal file structures are too fragile for tools like this one to reliably exist.

Valve can break third-party tools without a word of notice and never provide an official fix, leaving developers to flounder and have to reverse engineer the entirety of Steam to try and guess how to fix their projects to work with yet another stupid and unnecessary change Valve felt like making.

Larger teams working on larger projects may have the time and/or energy to figure these out. We do not. This project was created to fix a minor headache, and has instead mutated into a migraine of diabolical proportions.

Please consider the following alternatives:

- [UTL](https://github.com/thpatch/Universal-THCRAP-Launcher), which is an official part of thcrap that provides a simple game-select menu. With UTL, you only need to add the UTL exe itself to Steam just once, and then your Touhou games will then be available through a single shortcut in Steam.
- The [standalone patches](https://www.thpatch.net/wiki/Touhou_Patch_Center:Standalone_Patches), which give you individual .exe's for translated versions of each Touhou game that can be easily added to Steam.
- If you are adding the games to Steam just to have Steam Input enabled for them, you can use [GlosSI](https://github.com/Alia5/GlosSI) instead, or a system-wide gamepad mapper such as [AntiMicroX](https://github.com/AntiMicroX/antimicrox/).
- Adding the games manually -- add `thcrap_loader.exe` and, in Properties, set "Launch Options" to e.g. `en.js th06` (for EoSD in English).
- Using a [better launcher](https://playnite.link/).

If you are dead-set on using `steam-thcrap`, or are willing to take over its development, the original README follows below. 

---

![](https://repository-images.githubusercontent.com/580734620/d3bdc5b8-36ee-4b32-b35c-a6bf8c29074c)

# steam-thcrap
This is a small program to automatically add [thcrap](https://thpatch.net)-patched [Touhou](https://touhou-project.news) games to [Steam](https://s.team) as shortcuts ("Non-Steam Games").
It was created due to the fact that adding them manually these days can take a damn hour or so since there's tons of games and Steam's built-in shortcut editor is wildly inefficient for adding multiple games with custom launch arguments.

## Usage instructions
[Download](../../releases/latest/download/steam-thcrap.zip) the latest release, extract and place the `steam-thcrap` folder near `thcrap.exe`, and run the `steam-thcrap.exe` file inside. You are done.

## Build instructions (for developers only)
(in a command line prompt, with [Python](https://python.org) installed)

```batch
python -mvenv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
rem ... make and test your changes...
black steam-thcrap.py
pyinstaller --icon icon.ico steam-thcrap.py
xcopy grid dist\steam-thcrap\grid\
cd dist
python -m zipfile -c steam-thcrap.zip steam-thcrap/
```

## Alternatives
This program exploits internal, undocumented Steam functionality and as such may break, whether partially or completely, when Steam updates. We intend to try to fix it when such things happen, but there's a chance that some change Valve makes will break the program beyond repair.

While no other software (to the best of our knowledge) provides this exact functionality, you may find some other options helpful in case steam-thcrap breaks.
