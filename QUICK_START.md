# 🚀 Quick Start Guide

## Starting the Server

```bash
cd /Users/vinisha/Desktop/Buildbridge-AI/BridgeTales-AI
python3 run.py
```

## Accessing the Application

### 🎨 **Frontend (Beautiful Storybook Interface)**
Open your browser and go to:
```
http://localhost:8000/
```
or
```
http://127.0.0.1:8000/
```

This will show you the beautiful AI-powered storybook interface where you can:
- Type any theme you want
- Click quick action buttons (Kindness, Friendship, Adventure, etc.)
- Read your generated story
- Listen to the voice narration

### 🔧 **API Endpoints (For Direct API Access)**

If you want to use the API directly (returns JSON):
```
http://localhost:8000/story/generate?theme=kindness
```

Other useful endpoints:
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`
- API Info: `http://localhost:8000/api`

## What You're Currently Seeing

If you see JSON output like:
```json
{
  "theme": "kindness",
  "story": "Here is a heartwarming story...",
  "voice_file": "story_audio.mp3"
}
```

You're accessing the **API endpoint directly**. To see the beautiful frontend:

1. **Close that tab**
2. **Open a new tab**
3. **Go to:** `http://localhost:8000/` (just the root URL)

You should see a beautiful storybook interface with:
- "BridgeTales" title at the top
- 6 colorful quick action buttons
- A text input asking "What would you like your story to be about?"
- A "Generate Story" button

## Troubleshooting

**Q: I only see JSON output**
A: You're on the API endpoint. Go to `http://localhost:8000/` instead (without `/story/generate`)

**Q: Server won't start**
A: Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

**Q: CSS/styles not loading**
A: Make sure you're accessing `http://localhost:8000/` from the same directory where you ran the server.

## Features to Try

1. **Quick Actions**: Click any of the 6 theme buttons at the top
2. **Custom Theme**: Type your own theme and press Enter or click "Generate Story"
3. **Audio Player**: After the story generates, click the play button to hear it
4. **Share**: Click the "Share" button to copy your story
5. **New Story**: Click "New Story" to start over
