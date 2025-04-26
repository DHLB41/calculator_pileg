#!/bin/bash

# Setup Script for Simulasi Kalkulasi Pemilu 2029
# ==============================================

# Step 1: Create Virtual Environment
python3 -m venv venv

# Step 2: Activate Virtual Environment
source venv/bin/activate

# Step 3: Upgrade pip
pip install --upgrade pip

# Step 4: Install Requirements
pip install -r requirements.txt

# Step 5: Message
echo "\n✅ Environment setup complete!"
echo "🚀 To run the app, activate environment and run: streamlit run app.py"

echo "\n📂 Project Structure Reminder:"
echo "├── app.py"
echo "├── components/"
echo "├── utils/"
echo "├── assets/"
echo "├── data_calculated.xlsx"
echo "├── README.md"
echo "├── requirements.txt"
echo "└── setup.sh"

# End of setup
