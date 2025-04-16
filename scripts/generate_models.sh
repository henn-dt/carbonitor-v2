#!/bin/bash

# Name of the virtual environment
ENV_NAME="myenv"

# Path to the compatible Python binary (using the compiled Python 3.10)
/usr/local/bin/python3.10 -m venv $ENV_NAME

# Activate the virtual environment
source $ENV_NAME/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages with a compatible version of SQLAlchemy
pip install 'sqlalchemy<2.0' flask-sqlacodegen pymysql

# Generate models
DATABASE_URL="mysql+pymysql://carbonitor:henn@mysql_dt.henn.com/henn_carbonitor"
TABLES="products,buildups,models"
OUTPUT_FILE="models2.py"

flask-sqlacodegen $DATABASE_URL --tables $TABLES --outfile $OUTPUT_FILE

# Deactivate the virtual environment
deactivate

echo "Model generation complete. Models saved to $OUTPUT_FILE"