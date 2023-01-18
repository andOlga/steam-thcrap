import vdf
import json
import winreg
import os
import glob
import time
import binascii
import shutil


def main():
    handleSubdirectory()
    steamPath = getSteamPath()
    games, langs = getGames()
    sFiles = getShortcutFiles(steamPath)
    for sFile in sFiles:
        for lang in langs:
            for game, icon in games.items():
                if "_custom" not in game:
                    addShortcut(sFile, game, lang, icon)

    print("All done. Restarting Steam...")
    restartSteam(steamPath)


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
    "th185": "100th Black Market",
}

selfLocation = os.getcwd()


def handleSubdirectory():
    if not os.path.exists("thcrap.exe"):
        if os.path.exists("../thcrap.exe"):
            os.chdir("..")
        else:
            fail(
                "Failed to find thcrap. Make sure this application is placed in the thcrap folder."
            )


def getSteamPath():
    try:
        steamPath = winreg.QueryValueEx(
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam"),
            "SteamPath",
        )[0]
        if not steamPath:
            fail(
                "Failed to find Steam. Please run Steam at least once before continuing."
            )
        return steamPath
    except:
        fail("Failed to find Steam. Please run Steam at least once before continuing.")


def getGames():
    if not os.path.exists("config/games.js"):
        fail(
            "Failed to find thcrap config files. Please run thcrap.exe and configure your games before continuing."
        )
    games = json.load(open("config/games.js", "r", encoding="utf-8"))
    langs = [
        os.path.basename(x)
        for x in glob.glob("config/*.js")
        if os.path.basename(x) not in ["games.js", "config.js"]
    ]
    return games, langs


def getShortcutFiles(steamPath):
    sFiles = glob.glob(
        os.path.join(steamPath, "userdata", "**", "config", "shortcuts.vdf")
    )
    if not sFiles:
        fail(
            "Failed to find any shortcuts.vdf files. Please create at least one shortcut in Steam (to any game, not necessarily Touhou) manually before continuing."
        )
    return sFiles


def addShortcut(sFile, game, lang, icon):
    exePath = makeSteamPath(os.path.join(os.getcwd(), "thcrap_loader.exe"))
    configDir = os.path.dirname(sFile)
    userId = os.path.basename(os.path.dirname(configDir))
    shorts = vdf.binary_load(open(sFile, "rb"))["shortcuts"]
    short = {
        "AppName": makeAppName(game, lang),
        "Exe": exePath,
        "Icon": makeSteamPath(icon),
        "LaunchOptions": f"{lang} {game}",
    }
    if not checkGameExists(shorts, lang, game, exePath):
        print(f"Adding {short['AppName']} for user {userId}...")
        copyGameArt(short, game, configDir)
        short_index = str(max([int(x) for x in shorts.keys()]) + 1)
        shorts[short_index] = short
        vdf.binary_dump({"shortcuts": shorts}, open(sFile, "wb"))


def restartSteam(steamPath, timeout=10):
    os.system(f'"{steamPath}\\steam.exe" -shutdown')
    time.sleep(timeout)  # Wait for Steam to shut down
    os.system("start steam://open/games")


# Utility functions follow
def fail(err):
    print(err)
    os.system("pause")
    exit()


def makeSteamPath(path):
    return '"' + path.replace("/", "\\") + '"'


def makeAppName(game, lang):
    lang = lang.replace(".js", "")
    if name := names.get(game):
        longGame = game
        if len(longGame) > 4:
            longGame = longGame[:4] + "." + longGame[4:]
        longGame = longGame.replace("th", "Touhou ", 1)
        return f"{longGame} - {name} ({lang})"
    else:
        return f"{game} ({lang})"


def makeAppId(short):
    return str(binascii.crc32(str.encode(short["Exe"] + short["AppName"])) | 0x80000000)


def makeGridMap(short, game):
    appId = makeAppId(short)
    gd = {}
    for suffix in ["", "p", "_hero", "_logo"]:
        imageFile = None
        if os.path.exists(f"{selfLocation}/grid/{game}{suffix}.jpg"):
            imageFile = f"{selfLocation}/grid/{game}{suffix}.jpg"
        elif os.path.exists(f"{selfLocation}/grid/{game}{suffix}.png"):
            imageFile = f"{selfLocation}/grid/{game}{suffix}.png"
        if imageFile:
            gd[imageFile] = imageFile.replace(f"{selfLocation}/", "").replace(
                game, appId
            )
    return gd


def checkGameExists(shorts, lang, game, exePath):
    for short in shorts.values():
        if (
            short.get("Exe") == exePath
            and short.get("LaunchOptions") == f"{lang} {game}"
        ):
            return True
    return False


def copyGameArt(short, game, configDir):
    if not os.path.exists(os.path.join(configDir, "grid")):
        os.makedirs(os.path.join(configDir, "grid"))
    for src, dst in makeGridMap(short, game).items():
        shutil.copy(src, os.path.join(configDir, dst))


if __name__ == "__main__":
    main()
