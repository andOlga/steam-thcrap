names = {
    "th06": "the Embodiment of Scarlet Devil",
    "th07": "Perfect Cherry Blossom",
    "th075": "Immaterial and Missing Power",
    "th08": "Imperishable Night",
    "th09": "Phantasmagoria of Flower View",
    "th095": "Shoot the Bullet",
    "th10": "Mountain of Faith",
    "th105": "Scarlet Weather Rhaspody",
    "th11": "Subterranean Animism",
    "th12": "Undefined Fantastic Object",
    "th123": "Hisoutensoku",
    "th125": "Double Spoiler",
    "th128": "Fairy Wars",
    "th13": "Ten Desires",
    "th135": "Hopeless Masquerade",
    "th14": "Double Dealing Character",
    "th143": "Impossible Spell Card",
    "th145": "Urban Legend in Limbo",
    "th15": "Legacy of Lunatic Kingdom",
    "th155": "Antinomy of Common Flowers",
    "th16": "Hidden Star in Four Seasons",
    "th165": "Violet Detector",
    "th17": "Wily Beast and Wicked Creature",
    "th175": "Sunken Fossil World",
    "th18": "Unconnected Marketeers",
    "th185": "100th Black Market"
}

import vdf
import json
import winreg
import os
import glob

def fail(err):
    print(err)
    os.system("pause")
    exit()
def makeSteamPath(path):
    return '"' + path.replace('/', '\\') + '"'
def makeAppName(game, lang):
    lang = lang.replace('.js', '')
    if name := names.get(game):
        longGame = game
        if len(longGame) > 4:
            longGame = longGame[:4] + '.' + longGame[4:]
        longGame = longGame.replace('th', 'Touhou ', 1)
        return f"{longGame} - {name} ({lang})"
    else:
        return f"{game} ({lang})"

steamPath = winreg.QueryValueEx(
    winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam"),
    "SteamPath"
)[0]
if not steamPath:
    fail("Failed to find Steam. Please run Steam at least once before continuing.")
if not os.path.exists("config/games.js"):
    os.chdir('..')
if not os.path.exists("config/games.js"):
    fail("Failed to find thcrap config files. Please run thcrap.exe and configure your games before continuing.")
    os.system("pause")
    exit()
games = json.load(open("config/games.js", "r", encoding='utf-8'))
langs = [os.path.basename(x) for x in glob.glob("config/*.js") if os.path.basename(x) not in ["games.js", "config.js"]]

sFiles = glob.glob(os.path.join(steamPath, "userdata", "**", "config", "shortcuts.vdf"))
if not sFiles:
    fail("Failed to find any shortcuts.vdf files. Please create at least one shortcut in Steam (to any game, not necessarily Touhou) manually before continuing.")

for sFile in sFiles:
    shorts = vdf.binary_load(open(sFile, "rb"))['shortcuts']
    short_index = max([int(x) for x in shorts.keys()]) + 1
    for lang in langs:
        for game, icon in games.items():
            if "_custom" in game:
                continue
            name = names.get(game, '')
            short = {
                'AppName': makeAppName(game, lang),
                'Exe': makeSteamPath(os.path.join(os.getcwd(), 'thcrap_loader.exe')),
                'icon': makeSteamPath(icon),
                'LaunchOptions': f"{lang} {game}"
            }
            print(f"Adding {short['AppName']}...")
            shorts[str(short_index)] = short
            short_index += 1
    vdf.binary_dump({'shortcuts': shorts}, open(sFile, "wb"))
    fail("All done. Please restart Steam to see the Touhou games in your library.")
