echo off
cls
path "%CD%\node"
call npm install >nul 2>nul
node index.js
