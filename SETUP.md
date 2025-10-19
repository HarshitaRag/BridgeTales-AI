# 🚀 BridgeTales AI - Quick Setup Guide

## Step-by-Step Deployment

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/HarshitaRag/BridgeTales-AI.git
cd BridgeTales-AI
```

### 2️⃣ Set Up Environment Variables

```bash
# Copy the template
cp env.template .env

# Edit with your credentials
nano .env  # or use any text editor
```

Fill in your AWS credentials:
```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
PINECONE_API_KEY=pcsk_...  # Optional
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

**Option A: Use the deploy script**
```bash
./deploy.sh
```

**Option B: Run manually**
```bash
python3 run.py
```

### 5️⃣ Open Your Browser

Navigate to: **http://localhost:8000**

---

## 🎯 Quick Test

1. **Create your profile** (name, age, voice preference)
2. **Enter a story theme** (e.g., "adventure", "friendship")
3. **Click "Generate Story"**
4. **Make choices** to continue the adventure!
5. **Click on illustration** to find nearby cafes/parks
6. **Support local businesses** with demo Visa payment

---

## ⚙️ AWS Setup Requirements

### Required Services:

1. **AWS Bedrock**
   - Enable model access for:
     - `anthropic.claude-3-sonnet-20240229-v1:0`
     - `amazon.titan-image-generator-v1`

2. **AWS Polly**
   - No setup needed (included in AWS account)

3. **AWS Location Service**
   - Create a Place Index named: `HackathonPlaceIndex`
   - Choose data provider (Esri or HERE recommended)

### Optional Services:

4. **Pinecone**
   - Create free account at pinecone.io
   - Copy API key to `.env`

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9
python3 run.py
```

### AWS Credentials Not Working
- Check IAM permissions for Bedrock, Polly, Location Service
- Verify credentials in `.env` file
- Try region us-east-1 (best Bedrock support)

### Location Service Not Finding Businesses
- Create Place Index in AWS Console
- Name it: `HackathonPlaceIndex`
- Allow location access in browser

---

## 📞 Support

For issues or questions, check the main README.md or create an issue on GitHub.

**Happy Storytelling!** 📚✨

