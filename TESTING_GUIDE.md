# Testing Guide for New Features

## Quick Start

### 1. Setup Database
```bash
cd /c/Users/Dhiya/Desktop/PROJECTS/New-final-proj/new_story_app
python database_setup.py
```

Expected output:
```
--- Setting up database 'storyweaver.db'... ---
✓ Table 'child_profiles' created or already exists.
✓ Table 'story_sessions' created or already exists.
✓ Table 'button_clicks' created or already exists.
✓ Table 'audio_replays' created or already exists.
✓ Table 'quiz_results' created or already exists.
--- Database setup complete. ---
```

### 2. Start Backend
```bash
python app.py
```

The server should start on http://localhost:8000

### 3. Start Frontend
```bash
cd dream-narrate-web
npm run dev
```

The frontend should start on http://localhost:5173

## Testing Scenarios

### Test 1: Verify Hardcoded ID Fix

**Objective:** Confirm that the most recent child profile loads automatically

**Steps:**
1. Open the onboarding page (http://localhost:5173/)
2. Create a new child profile with a unique name (e.g., "Test Child 1")
3. Complete the onboarding form and submit
4. You should be redirected to the dashboard
5. Verify the dashboard shows "Test Child 1" profile
6. Create another profile with a different name (e.g., "Test Child 2")
7. Go back to dashboard
8. **Expected:** Dashboard should now show "Test Child 2" (most recent) without any code changes

**Success Criteria:**
- Dashboard always shows the most recently created child profile
- No need to update hardcoded IDs in the code

### Test 2: Story Duration Tracking

**Objective:** Verify that story duration is tracked from start to end

**Steps:**
1. From dashboard, select themes and language
2. Click "Start Story"
3. Note the time when story starts
4. Progress through the story (make choices)
5. Complete the story and quiz
6. Download the report
7. Open the JSON report and find the "duration_seconds" field

**Success Criteria:**
- Report shows accurate duration in seconds
- Duration matches approximately how long you spent on the story

### Test 3: Audio Controls

**Objective:** Test all audio control buttons and verify they work

**Steps:**
1. Start a story
2. Click the **Play** button (▶️) - audio should play
3. While audio is playing, click **Pause** button (⏸️) - audio should pause
4. Click **Play** again - audio should resume from where it paused
5. Click **Rewind** button (⏮️) - audio should jump back 10 seconds
6. Click **Forward** button (⏭️) - audio should jump forward 10 seconds
7. Click **Stop** button (🔇) - audio should stop

**Success Criteria:**
- All buttons work as expected
- Audio doesn't glitch or crash
- Controls are responsive

### Test 4: Audio Replay Counter

**Objective:** Verify that audio replays are counted and tracked

**Steps:**
1. Start a story
2. Look at the top of the page for "Audio Replays: 0"
3. Click Play to play audio for the first time (this shouldn't count as a replay)
4. After audio finishes, click Play again
5. **Expected:** Counter should show "Audio Replays: 1"
6. Play audio again
7. **Expected:** Counter should show "Audio Replays: 2"
8. Complete the story and download report
9. Check report for "total_audio_replays" field

**Success Criteria:**
- Counter increments correctly
- First play doesn't count as replay
- Subsequent plays count as replays
- Report shows correct total

### Test 5: Button Click Tracking

**Objective:** Verify all button clicks are tracked

**Steps:**
1. Start a story (this creates a session)
2. During the story:
   - Click audio controls multiple times
   - Make story choices
   - Use rewind/forward buttons
3. Complete the story
4. Submit quiz
5. Download report
6. Open the JSON report
7. Look at the "button_clicks" array

**Success Criteria:**
- All button clicks are listed with:
  - button_type (e.g., "audio_play", "choice_0", "audio_rewind")
  - part_number (which page of the story)
  - timestamp (when it was clicked)
  - count (how many times)

### Test 6: Quiz Functionality

**Objective:** Test end-of-story quiz generation and submission

**Steps:**
1. Start and complete a full story (reach part 5)
2. After the story ends, you should see "Preparing quiz..."
3. Quiz should appear with 3 questions
4. Answer all questions by clicking options
5. Click "Submit Quiz"
6. **Expected:** See score page with:
   - Your score (e.g., "You scored 2 out of 3!")
   - Audio replay count
   - "Download Report" and "Start New Story" buttons

**Success Criteria:**
- Quiz appears automatically after story completes
- All questions have multiple choice options
- Selected answers are highlighted
- Submit button is disabled until all questions are answered
- Score is calculated correctly
- Quiz results are in the report

### Test 7: Report Download

**Objective:** Verify comprehensive report generation

**Steps:**
1. Complete a full story with quiz
2. On the results page, click "Download Report"
3. A JSON file should download (e.g., "story_report_1.json")
4. Open the JSON file
5. Verify it contains:
   - session_info (child name, themes, duration, etc.)
   - button_clicks (all your interactions)
   - audio_replays (replay statistics)
   - quiz_results (questions, answers, correctness)
   - summary (totals)

**Success Criteria:**
- Report downloads successfully
- JSON is valid and readable
- All sections contain accurate data
- Timestamps are correct

### Test 8: Multiple Sessions

**Objective:** Verify tracking works across multiple story sessions

**Steps:**
1. Complete a full story session (Story 1)
2. Download the report - note the session_id
3. Go back to dashboard
4. Start a new story (Story 2)
5. Complete it and download that report too
6. **Expected:** Each report should have a different session_id
7. Each report should contain only data from that specific session

**Success Criteria:**
- Each session gets a unique ID
- Data doesn't mix between sessions
- Both reports are complete and accurate

## Database Verification

You can manually check the database to verify data is being stored:

```bash
cd /c/Users/Dhiya/Desktop/PROJECTS/New-final-proj/new_story_app
sqlite3 storyweaver.db
```

Then run these SQL queries:

```sql
-- View all sessions
SELECT * FROM story_sessions;

-- View all button clicks
SELECT * FROM button_clicks;

-- View all audio replays
SELECT * FROM audio_replays;

-- View all quiz results
SELECT * FROM quiz_results;

-- Get summary for a specific session (replace 1 with your session_id)
SELECT
  (SELECT COUNT(*) FROM button_clicks WHERE session_id = 1) as total_clicks,
  (SELECT COUNT(*) FROM audio_replays WHERE session_id = 1) as total_replays,
  (SELECT COUNT(*) FROM quiz_results WHERE session_id = 1 AND is_correct = 1) as correct_answers,
  (SELECT COUNT(*) FROM quiz_results WHERE session_id = 1) as total_questions;

-- Exit sqlite
.quit
```

## Common Issues & Solutions

### Issue: "Session not found" error
**Solution:** Make sure the story was started properly and session_id was returned from /start-story endpoint

### Issue: Audio controls don't work
**Solution:** Check browser console for Web Audio API errors. Some browsers require user interaction before audio can play.

### Issue: Quiz doesn't appear
**Solution:** Check backend logs for Gemini API errors. Ensure GOOGLE_API_KEY is set correctly in .env file

### Issue: Report download fails
**Solution:** Check that the session exists in the database and has data

### Issue: Button clicks not tracked
**Solution:** Verify network requests in browser DevTools. Check that session_id is being sent correctly.

## Performance Testing

For a complete test:
1. Complete 3 full stories
2. Each story should:
   - Take 5-10 minutes
   - Have 10+ button clicks
   - Have 2-3 audio replays
   - Complete the quiz
3. Download all 3 reports
4. Verify each report is unique and complete

## Success Metrics

After testing, you should have:
- ✅ 3+ child profiles in database
- ✅ 3+ completed sessions
- ✅ 30+ button click records
- ✅ 6+ audio replay records
- ✅ 9+ quiz results (3 questions × 3 sessions)
- ✅ 3 downloaded report files

All tracking data should be accurate and consistent!
