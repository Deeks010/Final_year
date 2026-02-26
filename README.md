# StoryWeaver - Interactive Story Generation App

An AI-powered educational storytelling application for children with autism. Generates personalized, interactive stories with text, images, and audio.

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Google Gemini API Key
- Cloudflare Worker API Token (for image generation)

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd new_story_app
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```


### 4. Configure Environment Variables

Create a `.env` file in the `new_story_app` directory with your API keys:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
CF_API_TOKEN=your_cloudflare_api_token
CF_IMAGE_URL=https://your-worker.your-account.workers.dev/
```

**Where to get API keys:**
- **GOOGLE_API_KEY**: https://aistudio.google.com/
- **CF_API_TOKEN**: Cloudflare Dashboard → Profile → API Tokens
- **CF_IMAGE_URL**: Your Cloudflare Worker endpoint

### 5. Set Up Frontend

```bash
cd dream-narrate-web
npm install
```

## Running the Application

### Step 1: Start Backend Server

Open a terminal and run:

```bash
# Make sure virtual environment is activated
cd new_story_app
venv\Scripts\activate

# Start FastAPI backend
python app.py
```

The backend server will start on **http://localhost:8000**

### Step 2: Start Frontend Development Server

Open a **new terminal** and run:

```bash
cd new_story_app/dream-narrate-web
npm run dev
```

You will see output like:

```
  VITE v5.4.19  ready in 244 ms

  ➜  Local:   http://localhost:8081/
  ➜  Network: http://172.25.67.146:8081/
```

**Note:** Port numbers may vary (8080, 8081, 8082, etc.) if ports are already in use.

## Accessing the Application

### On Your Laptop

Open browser and go to: `http://localhost:8081/` (or whatever port Vite shows)

### On Mobile Device (Same WiFi Network)

1. **Ensure both laptop and mobile are on the same WiFi**
2. Look at the Vite output and find the **Network URL**:
   ```
   ➜  Network: http://172.25.67.146:8081/
   ```
3. **Important:** Change the port number from `8081` to `8000`
4. Open mobile browser and navigate to: `http://172.25.67.146:8000/`

**Why port 8000?**
The frontend runs on port 8081 (or similar), but makes API calls to the backend on port 8000. The backend serves the built frontend, so accessing port 8000 gives you everything.

## Features

- **Personalized Stories**: Generated based on child's profile, interests, and autism characteristics
- **Interactive Choices**: Child makes decisions that affect the story
- **Multi-language Support**: English, Tamil, Hindi, and Tanglish
- **AI-Generated Images**: Visual illustrations for each story segment
- **Text-to-Speech**: Audio narration in multiple languages
- **Educational Themes**: Incorporates learning objectives like sharing, emotions, money management
- **Analytics Dashboard**: Track user engagement, button clicks, audio replays, and quiz performance

## User Activity Reports

User session reports are automatically generated and can be downloaded. Reports include:
- Session duration
- Button clicks tracking
- Audio replay counts
- Quiz performance
- Engagement metrics

Reports are saved as `session_report_*.json` files in the project directory.

## Project Structure

```
new_story_app/
├── app.py                 # Main FastAPI backend server
├── database_setup.py      # Database initialization
├── storyweaver.db        # SQLite database (auto-created)
├── .env                  # Environment variables (create this)
├── .env.example          # Template for .env file
├── requirements.txt      # Python dependencies
├── dream-narrate-web/    # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
└── tests/               # Test scripts

```

## Troubleshooting

### Backend won't start
- Check that `.env` file exists with valid API keys
- Verify virtual environment is activated
- Check if port 8000 is already in use

### Frontend won't start
- Run `npm install` in `dream-narrate-web/` directory
- Check if Node.js is installed: `node --version`

### Mobile can't connect
- Verify both devices are on the same WiFi network
- Check Windows Firewall isn't blocking port 8000
- Use the correct IP address from Vite's Network URL
- Remember to use port **8000**, not the port shown by Vite

### Images not generating
- Verify `CF_API_TOKEN` and `CF_IMAGE_URL` are correct in `.env`
- Check Cloudflare Worker is deployed and accessible

## Tech Stack

- **Backend**: FastAPI, Python 3.x
- **Frontend**: React, TypeScript, Vite, shadcn/ui, Tailwind CSS
- **AI Models**: Google Gemini 2.5 Flash
- **Image Generation**: Cloudflare Workers AI (Stable Diffusion)
- **Text-to-Speech**: Google Gemini TTS, Microsoft Edge TTS
- **Database**: SQLite

## License

This project is for educational purposes.
