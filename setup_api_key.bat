@echo off
echo ========================================
echo   SpaceSense - Gemini API Setup
echo ========================================
echo.
echo Get your FREE Gemini API key from:
echo https://makersuite.google.com/app/apikey
echo.
set /p API_KEY="Enter your Gemini API key: "

echo.
echo Setting environment variable...
setx GEMINI_API_KEY "%API_KEY%"

echo.
echo ✅ API key configured successfully!
echo.
echo NOTE: You may need to restart your terminal for changes to take effect.
echo.
pause
