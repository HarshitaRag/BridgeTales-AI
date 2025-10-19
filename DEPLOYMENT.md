# 🚀 Deployment Guide - BridgeTales AI

## 🎯 Deployment Options

BridgeTales AI is a **full-stack application** (Python backend + HTML/CSS/JS frontend), so you have several deployment options:

---

## ⚡ FASTEST: Render.com (5 minutes, FREE)

### Why Render?
- ✅ **Free tier** (perfect for hackathon demo)
- ✅ **Automatic deployment** from GitHub
- ✅ **HTTPS included**
- ✅ **Environment variables** built-in
- ✅ **No credit card** required

### Steps:

1. **Go to**: https://render.com
2. **Sign up** with GitHub account
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repo**: `HarshitaRag/BridgeTales-AI`
5. **Configure**:
   - **Name**: `bridgetales-ai`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python3 run.py`
   - **Port**: `8000`
6. **Add Environment Variables** (click "Advanced"):
   - `AWS_ACCESS_KEY_ID` = your_key
   - `AWS_SECRET_ACCESS_KEY` = your_secret
   - `AWS_REGION` = us-east-1
   - `PINECONE_API_KEY` = your_key (optional)
7. **Click "Create Web Service"**
8. **Wait 2-3 minutes** for deployment
9. **Done!** Your app will be at: `https://bridgetales-ai.onrender.com`

---

## 🌟 AWS Amplify (Production-Ready)

### Steps:

1. **Go to AWS Amplify Console**
2. **Connect GitHub repo**
3. **Auto-detects Python**
4. **Add environment variables**
5. **Deploy!**

**URL**: `https://main.xxxxx.amplifyapp.com`

---

## 🐳 Docker Deployment (Any Platform)

We need to create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "run.py"]
```

Then deploy to:
- **AWS ECS**
- **Google Cloud Run**
- **Azure Container Apps**
- **Railway.app**

---

## 📄 GitHub Pages (Frontend Only - Demo Purposes)

**NOTE**: This will show the frontend, but features won't work without backend!

### Steps:

1. **Go to your GitHub repo** settings
2. **Pages** → **Source**: Deploy from branch
3. **Branch**: `main`, folder: `/frontend`
4. **Save**
5. **Visit**: `https://harshitarag.github.io/BridgeTales-AI/`

**Limitation**: Stories won't generate (no Python backend on GitHub Pages)

---

## 🏆 RECOMMENDED FOR HACKATHON JUDGES

### Use Render.com Because:
1. ✅ **Free** (no cost to you)
2. ✅ **5 minute setup** (fastest deployment)
3. ✅ **Fully functional** (all features work)
4. ✅ **Shareable URL** (judges can test it themselves!)
5. ✅ **Auto-deploys** on Git push (just commit and it updates)

---

## 🎬 Live Demo URL

After deploying to Render, share this with judges:

```
🌐 Live Demo: https://bridgetales-ai.onrender.com
📂 GitHub: https://github.com/HarshitaRag/BridgeTales-AI
📋 Features: Age-appropriate AI stories + Local business discovery + Visa payments
```

---

## 🔧 Environment Variables Required

For any cloud platform, you'll need these:

```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
PINECONE_API_KEY=pcsk_... (optional)
```

---

## 📊 Cost Estimate

- **Render.com Free Tier**: $0/month (sleeps after 15min inactive)
- **AWS Amplify**: ~$10-20/month
- **Railway**: Free tier, then ~$5/month
- **Localhost**: FREE! (perfect for live demo)

---

## 💡 FOR YOUR HACKATHON DEMO

**Best Strategy**:
1. **Run localhost** during live presentation (`python3 run.py`)
2. **Deploy to Render** for judges to test later
3. **Keep GitHub clean** with good README

This way:
- ✅ **Live demo** works perfectly (localhost)
- ✅ **Judges can try it** after (Render URL)
- ✅ **Code is accessible** (GitHub)

---

## 🚨 Quick Deploy NOW (3 minutes)

```bash
# 1. Commit everything
git add .
git commit -m "Ready for deployment"
git push

# 2. Go to render.com
# 3. Connect GitHub
# 4. Add env vars
# 5. Deploy!
```

**Your app will be live in 3 minutes!** 🎉

