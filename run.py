#!/usr/bin/env python3
"""
BridgeTales AI API Server
Run this script to start the FastAPI server
"""

import uvicorn
from config import Config

if __name__ == "__main__":
    print("🚀 Starting BridgeTales AI API Server...")
    print(f"📍 Environment: {Config.ENVIRONMENT}")
    print(f"🌐 Host: {Config.API_HOST}:{Config.API_PORT}")
    
    # Validate configuration
    if not Config.validate_config():
        print("⚠️  Configuration validation failed. Please check your environment variables.")
        print("📝 Copy env.example to .env and fill in your API keys.")
    
    # Start the server
    uvicorn.run(
        "main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.ENVIRONMENT == "development",
        log_level=Config.LOG_LEVEL.lower()
    )
