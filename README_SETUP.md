# BridgeTales AI API Setup Guide

## Overview
BridgeTales is an AI-powered storytelling application with a beautiful storybook interface. It uses AWS Bedrock for story generation and ElevenLabs for voice narration, creating an immersive storytelling experience.

## Features
- ✅ Beautiful storybook-themed web interface
- ✅ Interactive theme input with quick action buttons
- ✅ FastAPI backend with automatic API documentation
- ✅ AWS Bedrock integration (primary AI)
- ✅ OpenAI integration (backup)
- ✅ ElevenLabs voice generation and narration
- ✅ Built-in audio player
- ✅ Responsive design for all devices
- ✅ Smooth animations and loading states
- ✅ Share functionality
- ✅ Health check endpoint
- ✅ CORS support
- ✅ Environment configuration
- ✅ Error handling and logging

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the example environment file and configure your API keys:
```bash
cp env.example .env
```

Edit `.env` file with your credentials:
```env
# AWS Configuration
AWS_REGION=us-east-2
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# OpenAI Configuration (backup)
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs Configuration (for voice generation)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 3. AWS Bedrock Setup
1. Ensure you have AWS credentials configured
2. Make sure you have access to AWS Bedrock in your region
3. The code uses Claude 3 Sonnet model - ensure it's available in your Bedrock account

### 4. Run the Server
```bash
python run.py
```

Or directly:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## Using the Application

### Web Interface
1. **Open your browser** and go to `http://localhost:8000`
2. **Enter a theme** in the input box (e.g., "friendship", "adventure", "magic")
3. **Click "Generate Story"** or use one of the quick action buttons
4. **Wait** for the AI to generate your story
5. **Read and listen** to your personalized story with voice narration
6. **Share** your story or create a new one!

### Quick Action Buttons
The interface includes preset theme buttons for quick story generation:
- Kindness
- Friendship
- Adventure
- Courage
- Magic
- Nature

## API Endpoints

### GET /story/generate
Generate a story based on a theme.

**Query Parameters:**
- `theme` (string, optional): The theme for the story (default: "kindness")

**Example Request:**
```
GET /story/generate?theme=kindness
```

**Response:**
```json
{
  "theme": "kindness",
  "story": "Once upon a time, in a small village nestled between rolling hills, there lived a young girl named Maya who had a heart full of kindness...",
  "voice_file": "story_audio.mp3"
}
```

### GET /health
Check the health status of the API and connected services.

### GET /
Root endpoint with API information.

### GET /docs
Interactive API documentation (Swagger UI).

## Configuration Options

- `AWS_REGION`: AWS region for Bedrock (default: us-east-1)
- `ENVIRONMENT`: development/production (affects auto-reload)
- `LOG_LEVEL`: DEBUG/INFO/WARNING/ERROR
- `API_HOST`: Server host (default: 0.0.0.0)
- `API_PORT`: Server port (default: 8000)

## Troubleshooting

### AWS Bedrock Issues
- Verify AWS credentials are properly configured
- Check that you have access to Bedrock in your region
- Ensure the Claude model is available in your Bedrock account

### OpenAI Backup Issues
- Verify your OpenAI API key is valid
- Check your OpenAI account has sufficient credits

### General Issues
- Check the `/health` endpoint to see which services are available
- Review server logs for detailed error messages
- Ensure all dependencies are installed correctly

## Development

The server supports auto-reload in development mode. Just run:
```bash
python run.py
```

API documentation is available at `http://localhost:8000/docs` when the server is running.
