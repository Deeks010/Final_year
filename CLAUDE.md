# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

StoryWeaver is an AI-powered interactive storytelling application for children with autism. It uses Google Gemini API to generate personalized stories with images and audio, featuring comprehensive tracking and analytics for caregivers.

## Architecture

### Tech Stack
- **Backend:** FastAPI (Python) with async/await
- **Frontend:** React with TypeScript, Vite, shadcn/ui components
- **Database:** SQLite with direct SQL queries
- **AI:** Google Gemini API for text and image generation
- **TTS:** Google Cloud Text-to-Speech
- **Audio:** Web Audio API for playback controls

### Key Components

**Backend (app.py):**
- FastAPI application with async request handling
- Gemini API integration for story generation and theme creation
- Cloudflare Workers AI for image generation
- Google TTS for audio narration
- SQLite database with manual SQL queries (no ORM)

**Frontend (dream-narrate-web/src/):**
- React SPA with react-router-dom
- Pages: Onboarding, Dashboard, Profile, StoryBook
- StoryBook component handles story playback with tracking

**Database Tables:**
- `child_profiles` - Child information and generated themes
- `story_sessions` - Story session tracking
- `button_clicks` - User interaction tracking
- `audio_replays` - Audio replay events
- `quiz_results` - End-of-story quiz performance

## Development Commands

### Backend Setup and Running

```bash
# Setup (from new_story_app directory)
cd /c/Users/Dhiya/Desktop/PROJECTS/New-final-proj/new_story_app

# Install dependencies
pip install -r requirements.txt

# Setup database (creates all tables)
python database_setup.py

# Configure environment variables
# Create .env file with:
# GOOGLE_API_KEY=your_gemini_api_key
# CF_API_TOKEN=cloudflare_api_token
# CF_IMAGE_URL=cloudflare_image_endpoint

# Run server
python app.py
# Server runs on http://0.0.0.0:8000
```

### Frontend Setup and Running

```bash
# Setup (from dream-narrate-web directory)
cd dream-narrate-web
npm install

# Development mode
npm run dev
# Runs on http://localhost:5173

# Production build
npm run build

# Lint
npm run lint
```

### Database Operations

```bash
# Recreate all tables
python database_setup.py

# Access database directly
sqlite3 storyweaver.db

# View schema
sqlite3 storyweaver.db ".schema"

# Query data
sqlite3 storyweaver.db "SELECT * FROM child_profiles;"
```

## Key Implementation Details

### Story Generation Flow

1. **Dashboard** → User selects themes and language → POST `/start-story`
2. **Backend** generates:
   - One-line story plan (Gemini)
   - First story part with choices (Gemini)
   - Image for the part (Cloudflare AI)
   - Audio narration (Google TTS)
   - Creates tracking session in database
3. **Response** returns: session_id, plan, story data, base64 image, base64 audio
4. **StoryBook** displays content and tracks all interactions
5. **Continue** → User makes choice → POST `/continue-story` → repeat steps 2-4
6. **Story End** (part 5) → Automatic quiz generation → Quiz submission → Report download

### Child Profile Auto-Loading

**Problem:** Previously hardcoded `active_child_id = 7`

**Solution:** Both `/profile` and `/start-story` endpoints now query:
```sql
SELECT * FROM child_profiles ORDER BY id DESC LIMIT 1
```
This always fetches the most recently created child profile, eliminating manual configuration.

### Tracking System

**Session Creation:**
- Automatically created in `/start-story` endpoint
- Returns session_id to frontend
- Frontend stores session_id for all subsequent tracking calls

**Tracking Points:**
- Button clicks: `/api/tracking/button-click`
- Audio replays: `/api/tracking/audio-replay`
- Session end: `/api/session/{session_id}/end`
- Quiz submission: `/api/quiz/submit`

**Report Generation:**
- GET `/api/session/{session_id}/report`
- Joins all tracking tables
- Generates JSON report with full session analytics
- Saves to file: `session_report_{session_id}.json`

### Audio Controls Implementation

**Web Audio API** is used for advanced playback controls:
- Play/Pause with resume capability
- Seek forward/backward (10-second increments)
- Stop and reset
- Time tracking for pause/resume

Base64 audio from backend is decoded and played using AudioContext.

### Quiz Generation

Uses Gemini API with structured output (JSON schema):
```python
quiz_schema = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "question": {"type": "STRING"},
            "options": {"type": "ARRAY"},
            "correct_answer": {"type": "STRING"}
        }
    }
}
```

Generates 3 questions based on story summary and educational theme.

## API Endpoints Reference

### Story Endpoints
- `GET /profile` - Get most recent child profile
- `POST /onboard` - Create new child profile and generate themes
- `POST /start-story` - Start new story session
- `POST /continue-story` - Continue to next story part

### Tracking Endpoints
- `POST /api/session/start` - Start tracking session (deprecated, use /start-story)
- `POST /api/session/{id}/end` - End session with duration
- `POST /api/tracking/button-click` - Track button interaction
- `POST /api/tracking/audio-replay` - Track audio replay
- `GET /api/session/{id}/report` - Generate and download report

### Quiz Endpoints
- `POST /api/quiz/generate` - Generate quiz questions
- `POST /api/quiz/submit` - Submit quiz answers and get score

## Common Pitfalls

1. **API Keys:** All three API keys must be set in environment variables:
   - GOOGLE_API_KEY (Gemini + TTS)
   - CF_API_TOKEN (Cloudflare)
   - CF_IMAGE_URL (Cloudflare endpoint)

2. **Base64 Encoding:** Images and audio are returned as base64 strings. Frontend must decode:
   ```typescript
   <img src={`data:image/jpeg;base64,${image_base64}`} />
   ```

3. **Session Management:** session_id MUST be passed from frontend for all tracking calls. It's returned in /start-story response.

4. **Audio Context:** Web Audio API requires user interaction before playing. First play must be triggered by user click.

5. **Database Queries:** Uses raw SQL, not an ORM. Always use parameterized queries to prevent SQL injection:
   ```python
   cursor.execute("SELECT * FROM table WHERE id = ?", (id,))
   ```

6. **Async Operations:** Backend uses async/await extensively. Always await async functions and use `async with aiohttp.ClientSession()` for API calls.

7. **Story Part Tracking:** Part numbers start at 1, not 0. Part 5 is the final part that triggers quiz generation.

## Working with the Codebase

### Adding New Tracking Metrics

1. Add column to appropriate table in `database_setup.py`
2. Run `python database_setup.py` to update database
3. Create new endpoint in `app.py` to receive tracking data
4. Add tracking call in `StoryBook.tsx` at appropriate interaction point
5. Update report generation to include new metric

### Modifying Story Generation

**Story length:** Change the part number check in `/continue-story` and `/start-story`

**Story themes:** Modify prompt in `themes_generator_agent_llm_call()` function

**Image style:** Modify `art_style_guide` parameter in frontend Dashboard.tsx

**Language support:** Add language to `supportedLanguages` array in Dashboard.tsx

### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Navigate using `navigate("/your-route")`

## Environment Variables

Required in `.env` file (backend):
```
GOOGLE_API_KEY=your_gemini_api_key_here
CF_API_TOKEN=your_cloudflare_token
CF_IMAGE_URL=https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0
```

Optional for frontend (`.env` in dream-narrate-web):
```
VITE_API_BASE_URL=http://localhost:8000
```

## Testing

Run the testing scenarios in `TESTING_GUIDE.md` to verify:
- Hardcoded ID fix works
- All tracking features work
- Audio controls function properly
- Quiz generates and submits correctly
- Reports download with complete data

## Recent Upgrades

See `UPGRADE_SUMMARY.md` for complete list of recent features added:
- ✅ Automatic child profile loading (no hardcoded IDs)
- ✅ Story duration tracking
- ✅ Enhanced audio controls (pause/play/rewind/forward)
- ✅ Button click tracking
- ✅ Audio replay counter
- ✅ End-of-story quiz
- ✅ Comprehensive JSON report export

## File Structure

```
new_story_app/
├── app.py                  # Main FastAPI application
├── database_setup.py       # Database schema and creation
├── requirements.txt        # Python dependencies
├── storyweaver.db         # SQLite database (auto-created)
├── CLAUDE.md              # This file
├── UPGRADE_SUMMARY.md     # Recent changes documentation
├── TESTING_GUIDE.md       # Testing instructions
└── dream-narrate-web/     # React frontend
    ├── src/
    │   ├── App.tsx
    │   ├── pages/
    │   │   ├── Onboarding.tsx
    │   │   ├── Dashboard.tsx
    │   │   ├── Profile.tsx
    │   │   └── StoryBook.tsx  # Main story playback (with tracking)
    │   └── components/ui/     # shadcn/ui components
    └── package.json
```

## Important Notes

- **DO NOT** hardcode child IDs anywhere - always fetch from database
- **DO NOT** commit API keys to git
- **ALWAYS** track user interactions for analytics
- **ALWAYS** use parameterized SQL queries
- **ALWAYS** await async functions in backend
- Frontend audio controls are mandatory for accessibility
- Session tracking is automatic - just pass session_id from initial response

## Support

For issues or questions:
1. Check `TESTING_GUIDE.md` for common problems
2. Review `UPGRADE_SUMMARY.md` for recent changes
3. Check backend console logs for API errors
4. Check browser console for frontend errors
5. Query database directly to verify data storage
