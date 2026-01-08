from mistralai import Mistral
from config.settings import settings
from config.logger import logger
from typing import List, Dict

class MistralService:
    def __init__(self):
        self.api_key = settings.MISTRAL_API_KEY
        if not self.api_key:
            logger.warning("MISTRAL_API_KEY is not set.")
        self.client = Mistral(api_key=self.api_key)

    async def chat_completion(self, messages: List[Dict[str, str]], model: str = None) -> str:
        """
        Send a chat request to Mistral API.
        messages: List of {"role": "...", "content": "..."}
        """
        model_to_use = model or settings.DEFAULT_MODEL
        logger.info(f"Sending request to Mistral API (model: {model_to_use})")
        
        try:
            # Mistral client typically synchronous, but we can wrap or use async client if available.
            # For simplicity in this step, we use the sync client call (fastapi handles it in threadpool).
            chat_response = self.client.chat.complete(
                model=model_to_use,
                messages=messages
            )
            logger.info("Received response from Mistral API")
            return chat_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling Mistral API: {e}", exc_info=True)
            return "Sorry, I encountered an error while processing your request."

mistral_service = MistralService()
