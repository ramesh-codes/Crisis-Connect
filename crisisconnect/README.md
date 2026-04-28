# CrisisConnect 🚨
**AI-Powered Rapid Disaster Alert & Resource Coordination Platform for India**

Built for the Rapid Crisis Response Open Innovation Challenge.

---

## Problem Statement
During disasters (floods, earthquakes, cyclones), emergency responders lack a fast, structured way to:
- Assess severity and scope quickly
- Get AI-generated response plans instantly
- Coordinate resources across agencies
- Track active alerts in real time

## Solution
CrisisConnect uses Google Gemini AI to analyze disaster reports and instantly generate:
- Severity assessment (LOW → CRITICAL)
- Step-by-step immediate action plans
- Resource requirements
- Evacuation recommendations
- Emergency contact numbers

## Tech Stack
- **Backend**: Python Flask
- **AI**: Google Gemini 2.5 Flash (via Google AI Studio)
- **Frontend**: Vanilla HTML/JS (no framework)
- **Deploy**: Google Cloud Run (containerized with Docker)

---

## Local Development

```bash
# 1. Clone and enter the project
cd crisisconnect

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Gemini API key (get free key at ai.google.dev)
export GEMINI_API_KEY="your_key_here"

# 5. Run locally
python app.py
# Visit http://localhost:8080
```

> **Note**: Works without an API key in demo mode with mock responses.

---

## Deploy to Google Cloud Run (Free Trial)

### Prerequisites
- Google Cloud account with ₹20,000 free credits
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed
- Docker installed (optional — Cloud Build handles it)

### Step 1: Set up Google Cloud project
```bash
# Login
gcloud auth login

# Create project (or use existing)
gcloud projects create crisisconnect-demo --name="CrisisConnect"
gcloud config set project crisisconnect-demo

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Step 2: Get Gemini API Key
1. Go to https://ai.google.dev/
2. Click "Get API key" → Create API key
3. Copy the key

### Step 3: Deploy
```bash
# Set your project and region
export PROJECT_ID="crisisconnect-demo"
export REGION="asia-south1"   # Mumbai — closest to India

# Build and deploy in one command using Cloud Build
gcloud run deploy crisisconnect \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY="YOUR_KEY_HERE" \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 3

# Done! You'll get a URL like:
# https://crisisconnect-xxxx-el.a.run.app
```

### Step 4: Verify deployment
```bash
# Check service status
gcloud run services describe crisisconnect --region $REGION

# Test health endpoint
curl https://YOUR-URL/health
```

---

## Cost Estimate (₹20,000 Free Credits — expires in ~55 days)
| Service | Usage | Cost |
|---------|-------|------|
| Cloud Run | ~50K requests/month | ~₹150 |
| Cloud Build | Build time (~3 builds) | ~₹50 |
| Gemini 2.5 Flash API | Free tier (10 RPM free) | ₹0 |
| **Total/month** | | **~₹200** |

> ⚠️ **Your credits expire in ~55 days.** Deploy within the next few days to maximize demo time.
> At ~₹200/month this prototype runs comfortably within your trial — but set a calendar reminder
> to either upgrade or shut down before expiry so you're not charged.

---

## GitHub Setup

```bash
# Initialize repo
git init
git add .
git commit -m "Initial commit: CrisisConnect prototype"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/crisisconnect
git branch -M main
git push -u origin main
```

---

## Project Structure
```
crisisconnect/
├── app.py              # Flask API + Gemini integration
├── static/
│   └── index.html      # Frontend (single file)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── .dockerignore       # Docker build exclusions
└── README.md           # This file
```

---

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Frontend app |
| POST | `/api/analyze` | Submit disaster report → get AI response |
| GET | `/api/alerts` | List all alerts |
| POST | `/api/alerts/:id/resolve` | Mark alert as resolved |
| GET | `/health` | Health check |

---

## Architecture
```
User → HTML Frontend → Flask API → Gemini 1.5 Flash
                             ↓
                     In-memory Alert Store
                     (upgrade to Firestore for production)
```

---

## Demo Video Script (suggested)
1. Show the live URL loading
2. Fill out a Flood report for Assam
3. Click "Analyze" → show AI response generating
4. Point out: severity badge, action steps, resources, contacts
5. Show the alert appearing in the feed
6. Resolve the alert
7. Mention: deployed on Cloud Run, powered by Gemini

---

## Future Improvements
- Firebase Firestore for persistent storage
- Google Maps integration for affected area visualization
- SMS alerts via Firebase/Twilio
- Multi-language support (Hindi, Bengali, Tamil)
- Resource inventory management
- Integration with NDMA API

---

Built with ❤️ for India's disaster response ecosystem.
