import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    # Default Mistral model (e.g., mistral-tiny, mistral-small, mistral-medium, or your fine-tuned ID)
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "mistral-tiny") 
    
    # Optional: Database config if needed later
    # DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
