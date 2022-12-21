const fd = require('node-file-dialog')
const ss = require('steam-shortcut-editor')
const fs = require('fs')
const names = require('./names.json')

function makeSteamPath (path) { // Converts a normal path into the Steam format
  return `"${path.replaceAll('/', '\\')}"`
}

async function main () {
  let steamDir = ''
  // Attempt to auto-detect Steam shortcuts location
  if (fs.existsSync('C:\\Program Files (x86)\\Steam')) {
    steamDir = 'C:\\Program Files (x86)\\Steam'
  } else {
    console.log('Please choose your Steam installation directory.')
    steamDir = (await fd({ type: 'directory' }))[0]
  }
  // Get thcrap game/language lists
  console.log('Please choose your thcrap directory.')
  const thCrapDir = (await fd({ type: 'directory' }))[0]
  const thGames = JSON.parse(fs.readFileSync(`${thCrapDir}/config/games.js`, 'utf-8'))
  const thLangs = fs.readdirSync(`${thCrapDir}/config`).filter(x => !['games.js', 'config.js'].includes(x))
  // Get Steam user directories
  const userDirs = fs.readdirSync(`${steamDir}/userdata`)
  // Start adding games
  for (const userDir of userDirs) {
    const shortFile = `${steamDir}/userdata/${userDir}/config/shortcuts.vdf`
    if (!fs.existsSync(shortFile)) {
      console.error(`Could not find ${shortFile}. The process may fail. If you never added any Steam shortcuts before, please add one and try again.`)
    }
    ss.parseFile(shortFile, (err, s) => {
      if (err) {
        console.error(err)
        return
      }
      for (const lang of thLangs) {
        for (const game of Object.keys(thGames)) {
          if (game.endsWith('_custom')) continue // Skip "custom" entries
          // Generate app name for Steam
          let appName = game
          if (appName.length > 4) appName = appName.slice(0, 4) + '.' + appName.slice(4) // "th095" -> "th09.5"
          appName = appName.replace('th', 'Touhou ') // "th09.5" -> "Touhou 09.5"
          if (names[game]) {
            appName += `: ${names[game]}` // "Touhou 09.5" -> "Touhou 09.5: Shoot the Bullet"
          }
          appName += ` (${lang.replace('.js', '')})` // "Touhou 09.5: Shoot the Bullet" -> "Touhou 09.5: Shoot the Bullet (en)"
          // Actually add the game
          console.log(`Adding ${appName}...`)
          const short = {
            AppName: appName,
            Exe: makeSteamPath(`${thCrapDir}/thcrap_loader.exe`),
            StartDir: makeSteamPath(thCrapDir),
            Icon: makeSteamPath(thGames[game]),
            LaunchOptions: `${lang} ${game}`
          }
          s.shortcuts.push(short)
        }
      }
      ss.writeFile(shortFile, s, err => { if (err) console.error(err) })
      console.log('All done, please restart Steam.')
      setTimeout(_ => {}, 5000) // Wait before closing app to ensure user sees message
    })
  }
}

main().catch(console.error)
