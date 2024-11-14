#!/bin/sh

echo "Starting data ingestion with config.yml..."
python src/pipeline/run.py config.yml

if [ $? -eq 0 ]; then
    echo "Data ingestion completed successfully."
    echo "Starting the Streamlit app..."
    streamlit run src/app/app.py --server.port=8502
else
    echo "Data ingestion failed. Streamlit app will not start."
    exit 1
fi