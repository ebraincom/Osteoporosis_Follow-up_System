@echo off
echo Testing backend startup...
cd backend-python
echo Current dir: %CD%
echo Checking Python...
python --version
echo Checking main_simple.py...
if exist main_simple.py (
    echo main_simple.py found
) else (
    echo main_simple.py not found
)
echo Starting backend...
python main_simple.py
pause 