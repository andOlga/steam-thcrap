# steam-thcrap
This is a small program to automatically add [thcrap](https://thpatch.net)-patched Touhou games to Steam as shortcuts ("Non-Steam Games").
It was created due to the fact that adding them manually these days can take a damn hour or so since there's tons of games and Steam's built-in shortcut editor is wildly inefficient for adding multiple games with custom launch arguments.

## Usage instructions
[Download](../../releases/latest/download/steam-thcrap.zip) the latest release, extract it, and double-click the `steam-thcrap.bat` file.

Follow on-screen instructions: you will be asked to choose your thcrap directory, and, if Steam can't be auto-detected, your Steam directory.

## Build instructions
1. Download the latest LTS version for node from nodejs.org for Windows, and extract it into the `node` directory.
2. Run `steam-thcrap.bat` at least once to confirm everything works.
3. Delete the `node_modules` directory.
4. Zip everything else up and distribute.
