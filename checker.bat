@echo off
python --version 3>NUL
if errorlevel 1 goto errorNoPython

goto damn

:damn
pip install -r requirements.txt
start builder.py
pause

pyinstaller -v>NUL
if errorlevel 1 goto admin

:errorNoPython
echo.
echo Error^: Python not installed or not added to path!
echo In order to fix this please install python and add it to path! (do not install python from the microsoft store)
echo.
pause

:admin
goto check_Permissions

:check_Permissions
    echo Administrative permissions required. Detecting permissions...
    echo.

    net session >nul 2>&1
    if %errorLevel% == 0 (
        goto :errorPath
    ) else (
        echo rerun with admin!
    )
    
    pause >nul


:errorPath
setx path "%path%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Scripts;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Scripts\;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\"
pause