# 🎪 BridgeTales AI - Interactive AI Storytelling for Kids

**AI-powered choose-your-own-adventure storybooks that help kids discover and support local businesses in their community!**

---

## 🌟 Features

- 📚 **Age-Appropriate Stories**: Stories automatically adapt vocabulary and complexity based on child's age
- 🔊 **Voice Narration**: Multiple AI voices (Ivy, Joanna, Matthew) with live demos
- 🎨 **AI-Generated Illustrations**: Unique images for each story page using AWS Bedrock
- 🗺️ **Local Business Discovery**: Find real cafes and parks near you using AWS Location Service
- 💳 **Visa Payment Demo**: Support local businesses with customizable payment amounts
- 👤 **User Profiles**: Save preferences (name, age, voice) to Pinecone
- 📖 **Dashboard**: View completed stories
- 🎯 **Interactive Choices**: True choose-your-own-adventure format

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS Account with access to:
  - AWS Bedrock (Claude, Titan Image Generator)
  - AWS Polly (Text-to-Speech)
  - AWS Location Service
- Pinecone API Key (optional)
- Google Places API Key (optional fallback)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/HarshitaRag/BridgeTales-AI.git
cd BridgeTales-AI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Optional: Pinecone for data storage
PINECONE_API_KEY=your_pinecone_api_key

# Optional: OpenAI as backup (not required)
# OPENAI_API_KEY=your_openai_api_key
```

4. **Run the application**
```bash
python3 run.py
```

5. **Open your browser**
```
http://localhost:8000
```

---

## 🎯 How It Works

1. **Create Profile**: Enter your name, age, and choose a voice
2. **Start Story**: Pick a theme (adventure, friendship, magic, etc.)
3. **Make Choices**: Select what happens next in the story
4. **Discover Local Businesses**: Click on illustrations to find nearby cafes and parks
5. **Support Locals**: Send demo Visa payments to support local businesses
6. **Save Stories**: Completed stories are saved to your dashboard

---

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS)
    ↓
FastAPI Backend
    ↓
├─ AWS Bedrock (Story Generation)
├─ AWS Polly (Voice Narration)
├─ AWS Titan (Image Generation)
├─ AWS Location Service (Business Discovery)
└─ Pinecone (Data Storage)
```

---

## 📁 Project Structure

```
BridgeTales-AI/
├── main.py                 # FastAPI application
├── run.py                  # Server startup script
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
│
├── services/
│   ├── story_generator.py      # AI story generation
│   ├── location_service.py     # AWS Location integration
│   └── google_location_service.py  # Google Places fallback
│
├── frontend/
│   ├── index.html         # Main storybook interface
│   ├── dashboard.html     # Completed stories dashboard
│   └── static/
│       ├── css/styles.css # Styling
│       └── js/app.js      # Frontend logic
│
├── voice_service.py       # AWS Polly integration
├── image_service.py       # AWS Bedrock image generation
└── pinecone_service.py    # Data persistence
```

---

## 🔑 AWS Setup

### 1. AWS Bedrock
- Enable Claude 3 Sonnet model access
- Enable Titan Image Generator model access

### 2. AWS Polly
- No special setup required (included in AWS account)

### 3. AWS Location Service
- Create a Place Index named `HackathonPlaceIndex`
- Choose data provider (e.g., Esri, HERE)

---

## 🎨 API Endpoints

- `GET /` - Main storybook interface
- `GET /story/generate?theme={theme}&voice={voice}&age={age}` - Generate new story
- `POST /story/continue` - Continue story with user's choice
- `GET /location/search?query={type}&latitude={lat}&longitude={lng}` - Find nearby businesses
- `POST /api/profile` - Save user profile
- `GET /api/voice-demo?voice={voice}` - Play voice sample
- `POST /api/save-book` - Save completed story

---

## 🌟 Key Technologies

- **FastAPI**: High-performance Python web framework
- **AWS Bedrock**: Claude 3 for story generation, Titan for images
- **AWS Polly**: Neural text-to-speech with child-friendly voices
- **AWS Location Service**: Real-time local business discovery
- **Pinecone**: Vector database for user profiles and stories
- **Vanilla JavaScript**: No framework overhead, fast and responsive

---

## 🎯 For Hackathon Judges

This project demonstrates:

1. **Multi-Service AWS Integration**: Bedrock, Polly, Location Service, Titan
2. **Real-World Impact**: Connects kids to local businesses in their community
3. **Age-Appropriate AI**: Dynamic content adjustment based on user age
4. **Interactive Storytelling**: True branching narratives with AI
5. **Full-Stack Implementation**: Backend API + Beautiful Frontend
6. **Data Persistence**: Pinecone integration for user data

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 👥 Contributors

Built with ❤️ for the AWS + Visa Hackathon

---

## 🐛 Troubleshooting

**Server won't start?**
- Make sure port 8000 is available: `lsof -ti:8000 | xargs kill -9`
- Check your `.env` file has valid AWS credentials

**No nearby businesses showing?**
- Make sure you've created the AWS Location Place Index
- Allow location access in your browser
- Check AWS Location Service permissions

**Stories not generating?**
- Verify AWS Bedrock model access is enabled
- Check AWS credentials are correct
- Ensure you're in a supported AWS region (us-east-1 recommended)

---

**Built with AWS Bedrock, AWS Polly, AWS Location Service, and lots of ☕**
