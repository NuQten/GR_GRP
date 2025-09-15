@echo off 

pushd "%~dp0.."

set VENV_DIR=.venv

if not exist %VENV_DIR% (
    echo Creating virtual environment...
    %USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe -m venv %VENV_DIR%
)

call "%VENV_DIR%\Scripts\activate"

if exist requirements.txt (
    echo Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

echo.
echo Running the application...
echo.
echo Step 1: Get Group List
echo -----------------------
echo.
python getGrList.py
echo Step 2: Get File HTML
echo -----------------------
echo.
python getFileHTML.py
echo Step 3: Get Data
echo -----------------------
echo.
python getData.py
echo Step 4: Get CSV
echo -----------------------
echo.
python getCSV.py
echo Finished!


deactivate

