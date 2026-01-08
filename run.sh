#!/bin/bash

echo "🔍 Activating environment variables"
set .env
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate environment variables."
    exit 1
else
    echo "✅ Environment variables activated successfully."
fi

echo "🚀 Preparing the data for finetuning."
python scripts/prepare_data.py
if [ $? -ne 0 ]; then
    echo "❌ Failed to prepare data."
    exit 1
else
    echo "✅ Data prepared successfully."
fi

echo "🚀 Starting the finetuning process."
python scripts/finetune_mistral.py
if [ $? -ne 0 ]; then
    echo "❌ Failed to start finetuning process."
    exit 1
else
    echo "✅ Finetuning process completed successfully."
fi

echo "🌐 Starting the FastAPI server."
# Run the FastAPI app
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
if [ $? -ne 0 ]; then
    echo "❌ Failed to start FastAPI server."
    exit 1
else
    echo "✅ FastAPI server started successfully."
fi
