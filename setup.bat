@echo off

REM Create .streamlit folder inside user directory
mkdir "%USERPROFILE%\.streamlit" 2>nul

REM Create config.toml file
(
echo [server]
echo port = %PORT%
echo enableCORS = false
echo headless = true
) > "%USERPROFILE%\.streamlit\config.toml"

echo Streamlit config created successfully.
