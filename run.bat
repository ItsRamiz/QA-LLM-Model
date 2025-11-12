@echo off
echo Checking if Ollama is installed...

ollama --version >nul 2>&1
if errorlevel 1 (
    echo Ollama is NOT installed. Please install it first from: https://ollama.ai
    pause
    exit /b
)

echo Ollama is installed.
echo Running the Model without a GPU could take approx 30min runtime.

set /p pull_model="Phi-4 model is required, install model ~ (9.4GB)? (y/n):"
if /i "%pull_model%"=="y" (
    echo Pulling Phi-4 model...
    ollama pull phi4

    echo.
    echo Running model.py...
    python model.py
) else (
    echo Exiting without pulling or running.
)

pause
