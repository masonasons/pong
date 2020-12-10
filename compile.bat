pyinstaller --add-data nvdaControllerClient64.dll;. --clean --onefile -w game.py --workpath winbuild --distpath windist
xcopy sounds windist/sounds /S /Y
xcopy docs windist /Y
rem xcopy ..\winfiles windist /S /Y
rmdir /S /Q winbuild
del game.spec
pause