# Mistral Model Finetuning & Property Assistant

A comprehensive FastAPI application designed to fine-tune a Mistral 7B model on real estate data and serve it via an interactive chat interface.

## 🚀 Overview

This project demonstrates how to:
1.  **Prepare Data**: Convert raw CSV property data into JSONL format suitable for Mistral's fine-tuning API.
2.  **Fine-tune**: Upload data and initiate a fine-tuning job using the Mistral SDK.
3.  **Serve**: Expose a chat API (`/api/chat`) and a web dashboard to interact with the model.
4.  **Monitor**: specific logging configurations for debugging and audit trails.

## 🛠️ Tech Stack

*   **Language**: Python 3.12+
*   **Framework**: FastAPI
*   **AI Provider**: Mistral AI (Official SDK)
*   **Frontend**: HTML5, Jinja2 Templates, Vanilla JS (for the chat UI)
*   **Server**: Uvicorn
*   **Configuration**: Pydantic Settings, Python-Dotenv

## 📂 Project Structure

Verified "Flat" Structure:

```text
mistral-model-finetuning/
├── classes/             # Pydantic models (ChatRequest, ChatResponse)
├── config/              # Configuration logic (Settings, Logger)
├── core/                # Core utilities
├── logs/                # Application logs (app.log)
├── routers/             # FastAPI routes (web.py, api.py)
├── scripts/             # Fine-tuning and data prep scripts
│   ├── finetune_mistral.py
│   └── prepare_data.py
├── services/            # Business logic (MistralService)
├── static/              # CSS, Images, JS assets
├── templates/           # HTML Templates (index.html)
├── .env.example         # Template for environment variables
├── main.py              # Application entry point
├── property_data.csv    # Source data for properties
├── requirements.txt     # Python dependencies
├── run.sh               # Helper script to launch the server
└── setup.py             # Setup file for editable install
```

## ⚙️ Setup & Installation

### 1. Prerequisites
*   Python 3.10 or higher.
*   A valid [Mistral API Key](https://console.mistral.ai/).

### 2. Clone & Install

**Option A: Automated Setup (Recommended)**
Use the provided setup script that handles everything automatically:

```bash
./setup.sh
```

This script will:
- Install all dependencies from `requirements.txt`
- Install the project in editable mode (`pip install -e .`)
- Set up the necessary directory structure

**Option B: Manual Setup**
If you prefer to install manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Install project in editable mode (Required for imports)
pip install -e .
```

### 3. Environment Configuration
Create a `.env` file in the root directory. You can copy the example:

```bash
cp .env.example .env
```

**Required Variables in `.env`**:
```ini
MISTRAL_API_KEY=your_actual_api_key_here
DEFAULT_MODEL=mistral-tiny  # Or your fine-tuned model ID
LOG_LEVEL=INFO
```

## 🏃‍♂️ How to Run

### 1. Start the Web Server
The easiest way is to use the provided shell script:

```bash
./run.sh
```
Or manually:
```bash
uvicorn main:app --reload
```

*   **Dashboard**: Open [http://127.0.0.1:8000](http://127.0.0.1:8000)
*   **API Docs**: Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Fine-tuning the Model
To train the model on your `property_data.csv`:

**Step A: Prepare Data**
Converts CSV to JSONL format in `scripts/`.
```bash
python scripts/prepare_data.py
```

**Step B: Start Fine-tuning**
Uploads data and starts the job.
```bash
python scripts/finetune_mistral.py
```
*   *Note*: The script currently sets `purpose="fine-tune"` for proper validation.
*   Check the logs or console output for the **Job ID**.

### 3. Using the Fine-tuned Model
Once the fine-tuning job is finished (status: `SUCCESS`):
1.  Copy the **Model ID** (e.g., `ft:mistral-tiny:your-id`).
2.  Update `DEFAULT_MODEL` in `.env` OR select it in the Web UI dropdown if configured.

## 🐛 Troubleshooting

*   **`ModuleNotFoundError`**: Run `pip install -e .` again. The project relies on being installed as a package.
*   **`401 Unauthorized`**: Check your `MISTRAL_API_KEY` in `.env`.
*   **Logging**: Check `logs/app.log` for detailed error traces.
*   **Validation Failed**: Ensure `scripts/prepare_data.py` generates valid JSONL (chat format) and `finetune_mistral.py` uses `purpose="fine-tune"`.

## 📝 Scripts Description

*   **`scripts/prepare_data.py`**: Reads `property_data.csv` and creates `training_data.jsonl` / `validation_data.jsonl`.
*   **`scripts/finetune_mistral.py`**: Interacts with Mistral API to upload files and create a fine-tuning job.
*   **`check_jobs.py`**: (Optional utility) Lists active fine-tuning jobs and their status.