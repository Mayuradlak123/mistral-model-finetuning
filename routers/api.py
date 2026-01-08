from fastapi import APIRouter, HTTPException
from classes.models import ChatRequest, ChatResponse
from services.mistral_service import mistral_service
from config.settings import settings
from config.logger import logger

mistral_router = APIRouter()

@mistral_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Chat endpoint called. Message count: {len(request.messages)}")
    try:
        # Convert pydantic models to dict list for the service
        messages_data = [{"role": m.role, "content": m.content} for m in request.messages]
        
        response_content = await mistral_service.chat_completion(
            messages=messages_data, 
            model=request.model
        )
        
        return ChatResponse(
            response=response_content,
            model_used=request.model or settings.DEFAULT_MODEL
        )
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
