:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython



:: Once done, exit the batch file -- skips executing the errorNoPython section

goto damn

:damn
start builder.py
pause

:errorNoPython
echo.
echo Error^: Python not installed or not added to path!
echo In order to fix this please install python and add it to path! (do not install python from the microsoft store)
pause