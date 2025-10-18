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
class StoryResponse(BaseModel):
    theme: str
    story: str

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
            "generate_story": "/story/generate?theme=your_theme",
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

@app.get("/story/generate", response_model=StoryResponse)
async def generate_story(theme: str = "kindness"):
    """Generate a story based on the provided theme"""
    try:
        # Validate theme
        if not theme or len(theme.strip()) < 2:
            raise HTTPException(
                status_code=400, 
                detail="Theme must be at least 2 characters long"
            )
        
        # Create a prompt based on the theme
        prompt = f"Write a short, engaging story about {theme}. Make it heartwarming and suitable for all ages."
        
        # Generate story
        result = await story_generator.generate_story(
            prompt=prompt,
            max_length=300,
            temperature=0.7
        )
        
        return StoryResponse(
            theme=theme,
            story=result["story"]
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
