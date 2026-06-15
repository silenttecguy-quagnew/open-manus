@echo off
cd /d E:\open-manus
echo ==================================================
echo   OpenManus ELITE - BOSS MODE KICKSTART
echo ==================================================
echo 1. Launch Interactive (Boss Mode)
echo 2. Launch Fully Autonomous (Kimi Swarm Mode)
echo ==================================================
set /p choice="Select Mode (1 or 2): "

if "%choice%"=="2" (
    echo Launching Fully Autonomous Elite Swarm...
    python main.py --autonomous
) else (
    echo Launching Interactive Elite Boss Mode...
    python main.py
)
pause
