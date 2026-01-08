import os
import time
import sys
from mistralai import Mistral
from dotenv import load_dotenv
from config.logger import logger

# Add project root path - REMOVED as we use pip install -e .
# from app.core.logger import logger

# Load env vars
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    logger.error("MISTRAL_API_KEY not found in environment variables.")
    # Assuming .env is in the project root, try to load it specifically if missing
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(project_root, ".env"))
    api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    # If still not found, exit
    print("FATAL: MISTRAL_API_KEY not found. Please check your .env file.")
    exit(1)

print(f"DEBUG: Loaded API Key: {api_key[:4]}...{api_key[-4:]} (Length: {len(api_key)})")


client = Mistral(api_key=api_key)

def upload_file(filepath):
    logger.info(f"Uploading {filepath}...")
    try:
        with open(filepath, "rb") as f:
            response = client.files.upload(file={
                "file_name": os.path.basename(filepath),
                "content": f.read(),
            }, purpose="fine-tune")
        logger.info(f"Uploaded {filepath}, ID: {response.id}")
        return response.id
    except Exception as e:
        logger.error(f"Failed to upload {filepath}: {e}")
        raise

def start_finetune():
    # Paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    training_file = os.path.join(script_dir, "training_data.jsonl")
    validation_file = os.path.join(script_dir, "validation_data.jsonl")
    
    if not os.path.exists(training_file) or not os.path.exists(validation_file):
        logger.error(f"Content files not found at {training_file}. Run prepare_data.py first.")
        return

    try:
        # Upload files
        train_file_id = upload_file(training_file)
        val_file_id = upload_file(validation_file)
        
        # Create job
        logger.info("Creating fine-tuning job...")
        created_job = client.fine_tuning.jobs.create(
            model="open-mistral-7b", 
            training_files=[{"file_id": train_file_id, "weight": 1}],
            validation_files=[val_file_id],
            hyperparameters={
                "training_steps": 100,
                "learning_rate": 0.0001
            },
            auto_start=False
        )
        
        logger.info(f"Job created successfully! Job ID: {created_job.id}")
        logger.info(f"Status: {created_job.status}")
        logger.info(f"Model Name (once complete): {created_job.fine_tuned_model}")
        logger.info("Use the Job ID to check status or start the job if auto_start=False.")
    except Exception as e:
        logger.error(f"Error starting fine-tune job: {e}")

if __name__ == "__main__":
    start_finetune()
