@echo off
:: This script installs MiKTeX on Windows.

:: Set variables
set MIKTEX_DOWNLOAD_URL=https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-x64.exe
set INSTALLER_NAME=basic-miktex-x64.exe

:: Change to the temporary directory
cd %TEMP%

:: Download the MiKTeX installer
echo Downloading MiKTeX installer...
powershell -Command "Invoke-WebRequest -Uri %MIKTEX_DOWNLOAD_URL% -OutFile %INSTALLER_NAME%" || (
    echo Failed to download MiKTeX installer.
    exit /b 1
)

:: Run the MiKTeX installer
echo Installing MiKTeX...
%INSTALLER_NAME% --silent || (
    echo MiKTeX installation failed.
    exit /b 1
)

:: Cleanup
echo Cleaning up...
del %INSTALLER_NAME%

:: Finish
echo MiKTeX installation completed successfully.
exit /b 0
