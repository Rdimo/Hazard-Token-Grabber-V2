@echo off
color 0a
echo.
set /p a="Enter the exe name : "
if [%a%]==[] ( 
    echo.
    echo bro enter a name
    pause
    EXIT /B 1
) 
if [%a%] NEQ [] (
    echo.
    echo Name is: %a%
    pyinstaller --clean --onefile --noconsole -i NONE --distpath ./ -n %a% main.py
    rmdir /s /q __pycache__
    rmdir /s /q build
    del /f / s /q %a%.spec
    echo.
    echo generated exe as %a%.exe in the current working directory
    echo.
    pause
    EXIT /B 1
)
