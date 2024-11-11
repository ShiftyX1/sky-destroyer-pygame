@echo off
echo Cleaning previous builds...
rmdir /s /q build dist
echo Building game...
pyinstaller build_game.spec --clean
echo Done!
pause