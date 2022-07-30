@echo off

color a

:check_Permissions2

    net session >nul 2>&1
    if %errorLevel% == 0 (
        echo YOU ARE RUNNING WITH ADMIN BE CAREFUL SINCE IT WILL EDIT PATH VARIABLES
        timeout 5
        goto poop
    ) else (
        goto poop
    )
    
    pause >nul

:poop
py --version 3>NUL
if errorlevel 1 goto errorNoPython

goto damn

:damn
pip install -r reqs.txt
pyinstaller -v>NUL
if errorlevel 1 goto admin
cls
cd %~dp0
set /p a="Enter the exe name (example = cheats) -> "
if [%a%]==[] ( 
    echo.
    echo bro enter a name
    pause
    EXIT /B 1
) 
if [%a%] NEQ [] (
    echo.
    echo Name is: %a%
    pyinstaller --clean --onefile --noconsole -i NONE -n %a% main.py
    rmdir /s /q __pycache__
    rmdir /s /q build
    del /f / s /q %a%.spec
    echo.
    echo generated exe as %a%.exe in the dist folder
    echo.
    pause
    EXIT /B 1
)
pause
exit /b 1

:errorNoPython
echo.
echo Error^: Python not installed or not added to path!
echo Adding python to Path for you!
echo.
pause
goto admin

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
setx path "%path%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Scripts;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Scripts\;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\"
pause
