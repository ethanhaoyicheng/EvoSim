@echo off
setlocal

echo ========================================
echo   EvoSim Windows Build + Butler Upload
echo ========================================
echo.

REM Ask for version unless supplied as first argument
if "%~1"=="" (
    set /p USER_VERSION=Enter version number: 
) else (
    set "USER_VERSION=%~1"
)

if "%USER_VERSION%"=="" (
    echo No version entered. Exiting.
    pause
    exit /b 1
)

echo.
echo Building Evolution Simulator v%USER_VERSION%...
echo.

REM Clean previous PyInstaller output
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build using the project spec file
pyinstaller --clean EvoSim.spec

if errorlevel 1 (
    echo.
    echo PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo Build complete.
echo.
echo Uploading v%USER_VERSION% to itch.io...
echo.

set "BUTLER=C:\Users\ethan\butler\butler.exe"

if not exist "%BUTLER%" (
    echo Butler was not found at:
    echo %BUTLER%
    echo.
    echo Edit the BUTLER path in this script.
    pause
    exit /b 1
)

"%BUTLER%" push "dist\EvoSim" "twinkledelux/evosim:windows" --userversion "%USER_VERSION%"

if errorlevel 1 (
    echo.
    echo Butler upload failed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build and upload successful!
echo   Version: %USER_VERSION%
echo ========================================
pause