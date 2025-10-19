from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import asyncio
from datetime import datetime
from voice_service import generate_voice_with_polly
from image_service import generate_images
# Import our story generation service and config
from services.story_generator import StoryGenerator
from services.location_service import LocationService
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

# Initialize services
story_generator = StoryGenerator()
location_service = LocationService()

# Track page counter for unique images
page_counter = 0

# Mount static files and frontend
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Request/Response Models
class StoryResponse(BaseModel):
    theme: str
    story: str
    voice_file: Optional[str] = ""
    images: List[str] = []
    location: str = ""
    choices: List[str] = []
    
class ProfileData(BaseModel):
    name: str
    age: int
    voice: str

class ContinueRequest(BaseModel):
    theme: str
    choice: str
    story_context: str
    is_ending: bool = False  # Flag to generate a happy ending
    voice: str = "Ivy"  # User's voice preference

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    services: dict

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    radius: Optional[int] = 5000
    max_results: Optional[int] = 10

class StoryLocationRequest(BaseModel):
    story_context: str
    latitude: float
    longitude: float
    max_results: Optional[int] = 5

class BusinessResponse(BaseModel):
    name: str
    address: str
    phone: Optional[str] = ""
    website: Optional[str] = ""
    categories: List[str] = []
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[float] = None

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend"""
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/dashboard.html", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard page"""
    with open("frontend/dashboard.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/api", response_model=dict)
async def api_info():
    """API information endpoint"""
    return {
        "message": "BridgeTales AI API",
        "version": "1.0.0",
        "endpoints": {
            "generate_story": "/story/generate?theme=your_theme",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/story_audio.mp3")
async def get_audio():
    """Serve the generated audio file"""
    audio_path = "story_audio.mp3"
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=404, detail="Audio file not found")

@app.get("/illustration_page_{page_num}.png")
async def get_illustration(page_num: int):
    """Serve the generated illustration image for a specific page"""
    image_path = f"illustration_page_{page_num}.png"
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Image file not found")

@app.post("/api/profile")
async def save_profile(profile: ProfileData):
    """Save user profile data"""
    # Save to Pinecone
    try:
        from pinecone_service import save_profile_to_pinecone
        await save_profile_to_pinecone(profile.dict())
    except Exception as e:
        print(f"Error saving to Pinecone: {e}")
    
    return {"status": "success", "message": "Profile saved", "profile": profile}

@app.get("/api/voice-demo")
async def voice_demo(voice: str, text: str):
    """Generate voice demo"""
    try:
        # Generate temp audio file
        audio_file = generate_voice_with_polly(text, voice_id=voice, output_file="demo_audio.mp3")
        if audio_file and os.path.exists(audio_file):
            return FileResponse(audio_file, media_type="audio/mpeg")
        else:
            raise HTTPException(status_code=500, detail="Voice demo generation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save-book")
async def save_book(book: dict):
    """Save completed book"""
    try:
        from pinecone_service import save_book_to_pinecone
        await save_book_to_pinecone(book)
        return {"status": "success", "message": "Book saved"}
    except Exception as e:
        print(f"Error saving book: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services = {
        "aws_bedrock": await story_generator.check_bedrock_connection(),
        "openai": await story_generator.check_openai_connection(),
        "aws_location": await location_service.check_location_service_connection()
    }
    
    return HealthResponse(
        status="healthy" if all(services.values()) else "degraded",
        timestamp=datetime.now(),
        services=services
    )

@app.get("/story/generate", response_model=StoryResponse)
async def generate_story(theme: str = "kindness", voice: str = "Ivy"):
    """Generate a story based on the provided theme"""
    global page_counter
    page_counter += 1  # Increment for each new story segment
    
    try:
        # Validate theme
        if not theme or len(theme.strip()) < 2:
            raise HTTPException(
                status_code=400, 
                detail="Theme must be at least 2 characters long"
            )
        
        # Create a prompt based on the theme
        prompt = f"An interactive adventure about {theme}"
        
        # Generate story with choices
        result = await story_generator.generate_story(
            prompt=prompt,
            max_length=1000,
            temperature=0.7,
            is_continuation=False
        )
        
        story_text = result["story"]
        location = result.get("location", "")
        choices = result.get("choices", [])
        
        # Generate voice narration with AWS Polly (child voice)
        voice_file = ""
        try:
            result_file = generate_voice_with_polly(story_text, voice_id=voice)
            if result_file:
                voice_file = result_file
        except Exception as e:
            print(f"⚠️ Voice generation failed: {e}")
        
        # Generate illustration with Bedrock Titan (unique per page)
        images = []
        try:
            image_prompt = f"Children's storybook illustration based on this story: {story_text[:200]}"
            images = generate_images(image_prompt, page_number=page_counter)
        except Exception as e:
            print(f"⚠️ Image generation failed: {e}")
        
        return StoryResponse(
            theme=theme,
            story=story_text,
            voice_file=voice_file,
            images=images,
            location=location,
            choices=choices
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Story generation failed: {str(e)}"
        )

@app.post("/story/continue", response_model=StoryResponse)
async def continue_story(request: ContinueRequest):
    """Continue the story based on user's choice"""
    global page_counter
    page_counter += 1  # Increment for each continuation
    
    try:
        # Validate request
        if not request.choice or len(request.choice.strip()) < 2:
            raise HTTPException(
                status_code=400, 
                detail="Choice must be provided"
            )
        
        # Check if this is a happy ending request
        if request.is_ending:
            # Generate a happy ending
            ending_prompt = f"{request.story_context}\n\nNow create a satisfying happy ending that wraps up the story beautifully. Make it heartwarming and conclusive with no more choices."
            result = await story_generator.generate_story(
                prompt=ending_prompt,
                max_length=1000,
                temperature=0.7,
                is_continuation=False
            )
            story_text = result["story"]
            choices = []  # No more choices after ending
        else:
            # Continue story based on choice
            result = await story_generator.generate_story(
                prompt=request.story_context,
                max_length=1000,
                temperature=0.7,
                is_continuation=True,
                previous_choice=request.choice
            )
            story_text = result["story"]
            choices = result.get("choices", [])
        
        # Generate voice narration with AWS Polly
        voice_file = ""
        try:
            result_file = generate_voice_with_polly(story_text, voice_id=request.voice)
            if result_file:
                voice_file = result_file
        except Exception as e:
            print(f"⚠️ Voice generation failed: {e}")
        
        # Generate illustration with Bedrock Titan (unique per page)
        images = []
        try:
            image_prompt = f"Children's storybook illustration based on this story: {story_text[:200]}"
            images = generate_images(image_prompt, page_number=page_counter)
        except Exception as e:
            print(f"⚠️ Image generation failed: {e}")
        
        return StoryResponse(
            theme=request.theme,
            story=story_text,
            voice_file=voice_file,
            images=images,
            choices=choices
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Story continuation failed: {str(e)}"
        )

@app.post("/location/nearby", response_model=List[BusinessResponse])
async def get_nearby_businesses(request: LocationRequest):
    """Get nearby businesses based on user location"""
    try:
        businesses = await location_service.search_nearby_businesses(
            latitude=request.latitude,
            longitude=request.longitude,
            radius=request.radius,
            max_results=request.max_results
        )
        
        return [BusinessResponse(**business) for business in businesses]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find nearby businesses: {str(e)}"
        )

@app.post("/location/story-related", response_model=List[BusinessResponse])
async def get_story_related_businesses(request: StoryLocationRequest):
    """Get businesses related to story context"""
    try:
        businesses = await location_service.find_story_related_businesses(
            story_context=request.story_context,
            latitude=request.latitude,
            longitude=request.longitude,
            max_results=request.max_results
        )
        
        return [BusinessResponse(**business) for business in businesses]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find story-related businesses: {str(e)}"
        )

@app.get("/location/search")
async def search_businesses_by_text(
    query: str,
    latitude: float,
    longitude: float,
    max_results: int = 10
):
    """Search for businesses by text query"""
    try:
        businesses = await location_service.search_businesses_by_text(
            search_text=query,
            latitude=latitude,
            longitude=longitude,
            max_results=max_results
        )
        
        return [BusinessResponse(**business) for business in businesses]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search businesses: {str(e)}"
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
