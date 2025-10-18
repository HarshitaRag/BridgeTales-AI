from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import asyncio
from datetime import datetime

# Import our story generation service and config
from services.story_generator import StoryGenerator
from config import Config

app = FastAPI(
    title="BridgeTales AI API",
    description="AI-powered story generation API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize story generator
story_generator = StoryGenerator()

# Request/Response Models
class StoryRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 500
    temperature: Optional[float] = 0.7
    genre: Optional[str] = None
    characters: Optional[List[str]] = None
    setting: Optional[str] = None

class StoryResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    story: str
    generated_at: datetime
    model_used: str
    prompt_used: str
    word_count: int

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    services: dict

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "BridgeTales AI API",
        "version": "1.0.0",
        "endpoints": {
            "generate_story": "/generate_story",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services = {
        "aws_bedrock": await story_generator.check_bedrock_connection(),
        "openai": await story_generator.check_openai_connection()
    }
    
    return HealthResponse(
        status="healthy" if all(services.values()) else "degraded",
        timestamp=datetime.now(),
        services=services
    )

@app.post("/generate_story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    """Generate a story based on the provided prompt and parameters"""
    try:
        # Validate request
        if not request.prompt or len(request.prompt.strip()) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Prompt must be at least 10 characters long"
            )
        
        # Generate story
        result = await story_generator.generate_story(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature,
            genre=request.genre,
            characters=request.characters,
            setting=request.setting
        )
        
        return StoryResponse(
            story=result["story"],
            generated_at=datetime.now(),
            model_used=result["model_used"],
            prompt_used=request.prompt,
            word_count=len(result["story"].split())
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Story generation failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    # Validate configuration on startup
    Config.validate_config()
    
    uvicorn.run(
        app, 
        host=Config.API_HOST, 
        port=Config.API_PORT,
        log_level=Config.LOG_LEVEL.lower()
    )
