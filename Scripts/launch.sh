#!/bin/bash

# --------------------------------------------------
# Se placer dans le dossier parent du script
# --------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# --------------------------------------------------
# Nom du venv
# --------------------------------------------------
VENV_DIR=".venv"

# --------------------------------------------------
# 1. Création du venv si nécessaire
# --------------------------------------------------
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# --------------------------------------------------
# 2. Activation du venv
# --------------------------------------------------
source "$VENV_DIR/bin/activate"

# --------------------------------------------------
# 3. Installation des dépendances si requirements.txt existe
# --------------------------------------------------
if [[ -f "requirements.txt" ]]; then
    echo "Installing dependencies..."
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
fi

# --------------------------------------------------
# 4. Exécution des scripts Python
# --------------------------------------------------
echo
echo "Running the application..."
echo

echo "Step 1: Get Group List"
echo "-----------------------"
python3 getGrList.py
echo

echo "Step 2: Get File HTML"
echo "-----------------------"
python3 getFileHTML.py
echo

echo "Step 3: Get Data"
echo "-----------------------"
python3 getData.py
echo

echo "Step 4: Get CSV"
echo "-----------------------"
python3 getCSV.py
echo

echo "Finished!"

# --------------------------------------------------
# 5. Désactivation du venv
# --------------------------------------------------
deactivate
