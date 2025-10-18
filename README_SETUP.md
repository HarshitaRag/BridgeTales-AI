# BridgeTales AI API Setup Guide

## Overview
This FastAPI backend provides a `/generate_story` endpoint that connects to AWS Bedrock for AI story generation, with OpenAI as a backup option.

## Features
- ✅ FastAPI backend with automatic API documentation
- ✅ AWS Bedrock integration (primary)
- ✅ OpenAI integration (backup)
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
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# OpenAI Configuration (backup)
OPENAI_API_KEY=your_openai_api_key_here

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
  "story": "Once upon a time, in a small village nestled between rolling hills, there lived a young girl named Maya who had a heart full of kindness..."
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
