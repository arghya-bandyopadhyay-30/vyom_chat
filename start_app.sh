#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

# Run the data ingestion script
echo "Starting data ingestion..."
python src/pipeline/run.py config.yml

# Run the Streamlit application
echo "Starting the Streamlit app..."
streamlit run src/app/app.py --server.port=8502
