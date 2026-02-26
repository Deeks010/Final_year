# import json
# import time
# import os
# import asyncio
# import aiohttp
# from dotenv import load_dotenv

# # --- SETUP AND CONFIGURATION ---

# # Load environment variables from a .env file
# load_dotenv()
# API_KEY = os.getenv("GOOGLE_API_KEY")
# API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"


# # --- MOCK DATA AND PROFILES ---

# def get_child_profile():
#     """
#     Provides mock data for a child's profile.
#     In a real app, this would come from a database.
#     """
#     return {
#         "name": "Leo",
#         "age": 6,
#         "verbal_knowledge": "intermediate",
#         "interests": ["trains", "dinosaurs", "bright colors"],
#         "preferences": "visual stimulation, predictable routines",
#         "favorite_activities": ["building with blocks", "watching cartoons"],
#         "autism_severity": "Mild",
#         "communication_level": "Uses short sentences"
#     }

# # --- GEMINI API COMMUNICATION ---

# async def make_gemini_request(session, payload, is_json_response=False):
#     """
#     Makes an asynchronous request to the Gemini API with exponential backoff.
#     """
#     max_retries = 5
#     delay = 1  # Initial delay in seconds

#     headers = {'Content-Type': 'application/json'}

#     # If a structured JSON response is expected, add the generationConfig
#     if is_json_response:
#         payload['generationConfig'] = {
#             "responseMimeType": "application/json",
#             "responseSchema": {
#                 "type": "OBJECT",
#                 "properties": {
#                     "story_part": {"type": "STRING", "description": "The next part of the story, written in simple language."},
#                     "question": {"type": "STRING", "description": "A simple question to ask the child about what happens next."},
#                     "options": {
#                         "type": "ARRAY",
#                         "items": {"type": "STRING"},
#                         "description": "Three simple and distinct choices for the child."
#                     }
#                 },
#                 "required": ["story_part", "question", "options"]
#             }
#         }
    
#     for attempt in range(max_retries):
#         try:
#             async with session.post(API_URL, headers=headers, data=json.dumps(payload)) as response:
#                 if response.status == 200:
#                     result = await response.json()
#                     if not result.get('candidates'):
#                         print("API Error: Response is missing 'candidates'. Full response:", result)
#                         return None
                    
#                     text_content = result['candidates'][0]['content']['parts'][0]['text']
                    
#                     if is_json_response:
#                         return json.loads(text_content)
#                     else:
#                         return text_content
#                 else:
#                     print(f"API Error: Status {response.status}. Response: {await response.text()}")
#                     if response.status == 429: # Rate limited
#                          print(f"Rate limited. Retrying in {delay} seconds...")
#                          await asyncio.sleep(delay)
#                          delay *= 2
#                     else:
#                         return None # Fail on other errors
#         except aiohttp.ClientError as e:
#             print(f"Network Error: {e}")
#             if attempt < max_retries - 1:
#                 await asyncio.sleep(delay)
#                 delay *= 2
#             else:
#                 print("Max retries reached. Failing.")
#                 return None
#     return None

# # --- AGENT FUNCTIONS (API CALLERS) ---

# async def planner_agent_llm_call(session, prompt):
#     """
#     Makes a real LLM call to generate a one-line story plan.
#     """
#     print("--- Calling Planner Agent to generate a story plan... ---")
#     payload = {"contents": [{"parts": [{"text": prompt}]}]}
#     response_text = await make_gemini_request(session, payload)
#     print("------------------------------------------------------\n")
#     return response_text.strip() if response_text else "A default story about a friendly robot learning to share."

# async def story_generator_agent_llm_call(session, prompt):
#     """
#     Makes a real LLM call to generate a part of the story in JSON format.
#     """
#     print("--- Calling Story Generator Agent for the next part... ---")
#     payload = {"contents": [{"parts": [{"text": prompt}]}]}
#     response_json = await make_gemini_request(session, payload, is_json_response=True)
#     print("---------------------------------------------------------\n")
#     # Provide a fallback if the API call fails
#     if response_json:
#         return response_json
#     else:
#         return {
#             "story_part": "Oh no, the storybook page is blank! Let's try this instead: A friendly robot found a shiny red ball.",
#             "question": "What should the robot do?",
#             "options": ["Pick up the ball", "Look for the owner", "Leave the ball"]
#         }


# # --- CORE STORY GENERATION LOGIC ---

# async def generate_one_line_story_plan(session, child_profile, personalized_theme, educational_theme):
#     """
#     Creates a prompt and calls the planner agent to get a story plan.
#     """
#     prompt = f"""
#     Generate a simple, one-line story plan for a child with the following profile:
#     - Name: {child_profile['name']}
#     - Age: {child_profile['age']}
#     - Interests: {', '.join(child_profile['interests'])}
#     - Autism Severity: {child_profile['autism_severity']}
#     - Communication Level: {child_profile['communication_level']}

#     The story must combine these two themes:
#     - Personalized Theme: {personalized_theme}
#     - Educational Theme: {educational_theme}

#     The plan must be a single, simple sentence that sets up a situation or challenge.
#     """
#     one_line_plan = await planner_agent_llm_call(session, prompt)
#     return one_line_plan

# async def generate_interactive_story_part(session, one_line_plan, story_history, child_choice, part_number, language):
#     """
#     Generates the next part of the story, a question, and options.
#     """
#     prompt = f"""
#     You are a storyteller for an app designed for autistic children. Your language must be very simple, clear, and encouraging. Use short sentences.

#     Story Plan: "{one_line_plan}"
#     Target Language: {language}
    
#     Here is the story so far:
#     {story_history}

#     The child just made this choice: "{child_choice}"

#     Now, continue the story by writing Part {part_number} of 5. The story part should be a short paragraph.
    
#     After writing the story part:
#     1. Ask a simple question that lets the child decide what happens next.
#     2. Provide 3 simple, distinct options for the child to choose from.
    
#     Your entire response MUST be in the requested JSON format.
#     """
#     story_element = await story_generator_agent_llm_call(session, prompt)
#     return story_element

# # --- MAIN EXECUTION ---

# async def main():
#     """
#     Main function to run the interactive story generation flow.
#     """
#     # 1. Setup
#     child_profile = get_child_profile()
    # personalized_theme = "Dinesh and daniel go on a train adventure"
    # educational_theme = "money management"
    # target_language = "simple tamil(written in english)"
    
#     print("--- STORY SETUP ---")
#     print(f"Child: {child_profile['name']}")
#     print(f"Personalized Theme: {personalized_theme}")
#     print(f"Educational Theme: {educational_theme}\n")
    
#     async with aiohttp.ClientSession() as session:
#         # 2. Generate the one-line plan
#         plan = await generate_one_line_story_plan(session, child_profile, personalized_theme, educational_theme)
#         print("--- Generated Story Plan ---")
#         print(plan)
#         print("--------------------------\n")

#         # 3. Iteratively generate the 5-part story
#         full_story_history = ""
#         user_choice = "Let's begin the story!"

#         for i in range(1, 6):
#             part_number = i
#             print(f"--- Generating Part {part_number}/5 ---")
            
#             time.sleep(1) # Small delay for better user experience
            
#             story_part_data = await generate_interactive_story_part(
#                 session, plan, full_story_history, user_choice, part_number, target_language
#             )
            
#             print("\n--- Story Segment ---")
#             print(story_part_data["story_part"])
#             print("---------------------\n")
            
#             full_story_history += story_part_data["story_part"] + "\n"

#             print("--- Interactive Question ---")
#             print(story_part_data["question"])
#             for idx, option in enumerate(story_part_data["options"]):
#                 print(f"{idx + 1}. {option}")
#             print("---------------------------\n")

#             if part_number < 5:
#                 choice_index = -1
#                 while choice_index not in range(len(story_part_data["options"])):
#                     try:
#                         user_input = input(f"Enter your choice (1-{len(story_part_data['options'])}): ")
#                         choice_index = int(user_input) - 1
#                         if choice_index not in range(len(story_part_data["options"])):
#                             print("That's not a valid choice. Please pick a number from the list.")
#                     except ValueError:
#                         print("Please enter a number.")
                
#                 user_choice = story_part_data["options"][choice_index]
#                 print(f"--> You chose: '{user_choice}'\n")
#             else:
#                 print("The story is complete! Well done!")

# if __name__ == "__main__":
#     if not API_KEY:
#         print("ERROR: The GEMINI_API_KEY environment variable is not set.")
#         print("Please create a .env file and add your key, like this:")
#         print('GEMINI_API_KEY="YOUR_API_KEY_HERE"')
#     else:
#         try:
#             asyncio.run(main())
#         except KeyboardInterrupt:
#             print("\nStory generation cancelled.")


from http.client import HTTPException
import json
import time
import os
import asyncio
from xmlrpc import client
import aiohttp
import base64
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import edge_tts           # Microsoft Edge TTS — supports Tamil, Hindi, English, Tanglish
from google import genai  # Gemini TTS — used as primary for Tanglish (better quality)
from google.genai import types
import wave               # WAV helper for Gemini TTS output
import sqlite3            # SQLite database


# --- SETUP AND CONFIGURATION ---
# Load environment variables from a .env file
load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")
GEMINI_API_KEY = API_KEY
if not API_KEY:
    print("ERROR: GOOGLE_API_KEY environment variable not set.")
TEXT_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

# Cloudflare Worker for image generation
CF_API_TOKEN = os.environ.get("CF_API_TOKEN")
CF_IMAGE_URL = os.environ.get("CF_IMAGE_URL")

app = FastAPI()

# Allow requests from your React frontend (running on localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # <-- CHANGE THIS LINE
    allow_credentials=True,
    allow_methods=["*"], # Allow all standard methods
    allow_headers=["*"], # Allow all standard headers
)

class StoryStartRequest(BaseModel):
    personalized_theme: str
    educational_theme: str
    language: str
    art_style_guide: str

class StoryContinueRequest(BaseModel):
    one_line_plan: str
    story_context_history: list
    child_choice: str
    part_number: int
    language: str
    art_style_guide: str
class OnboardingProfile(BaseModel):
    name: str
    age: int
    interests: str
    favoriteActivities: str
    autismSeverity: str
    communicationLevel: str
# --- MOCK DATA AND PROFILES --- (UNCHANGED)

# def get_child_profile():
#     return {
#         "name": "Leo",
#         "age": 6,
#         "verbal_knowledge": "intermediate",
#         "interests": ["trains", "dinosaurs", "bright colors"],
#         "preferences": "visual stimulation, predictable routines",
#         "favorite_activities": ["building with blocks", "watching cartoons"],
#         "autism_severity": "Mild",
#         "communication_level": "Uses short sentences"
#     }



def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('storyweaver.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_child_profile(child_id: int):
    """
    Fetches a specific child profile from the database by their ID,
    parsing the personalized_themes JSON string into a list.
    """
    print(f"--- Fetching child profile for id={child_id} from database... ---")
    conn = get_db_connection()
    # MODIFIED: Query now uses WHERE id = ?
    profile_row = conn.execute('SELECT * FROM child_profiles WHERE id = ?', (child_id,)).fetchone()
    conn.close()
    
    if profile_row is None:
        print(f"--- No child profile found for id={child_id}. ---")
        return None
    
    profile_dict = dict(profile_row)
    print(f"--- Found profile: {profile_dict['name']} ---")

    try:
        themes_json = profile_dict.get('personalized_themes')
        if themes_json:
            profile_dict['personalized_themes'] = json.loads(themes_json)
        else:
            profile_dict['personalized_themes'] = []
    except (json.JSONDecodeError, TypeError):
        print(f"Warning: Could not parse themes for profile id {profile_dict['id']}.")
        profile_dict['personalized_themes'] = []
        
    return profile_dict

# --- NEW: Gemini agent function for generating themes ---
async def themes_generator_agent_llm_call(session, profile_data: dict):
    """
    Makes a Gemini API call to generate personalized story themes.
    """
    print("--- Calling Themes Generator Agent... ---")
    prompt = f"""
    Based on the following profile for a child, generate 10 simple, engaging, and personalized story themes.
    The themes should be short, one-sentence ideas (each within 3-5 words).
    
    Child's Profile:
    - Age: {profile_data.get('age')}
    - Interests: {profile_data.get('interests')}
    - Favorite Activities: {profile_data.get('favoriteActivities')}

    Return ONLY the 10 themes as a valid JSON array of strings. For example:
    ["A story about a friendly dinosaur who finds a magical train", "An adventure to find a lost rocket ship", "A tale of sharing colorful building blocks with a new friend","the journey of a talking car learning to help others", "A magical forest where toys come to life", "A day at the zoo with a mischievous monkey", "The secret clubhouse of adventurous kids", "A treasure hunt on a sunny island", "The little robot who wanted to dance", "A magical paintbrush that brings drawings to life"]
    """
    
    themes_schema = { "type": "ARRAY", "items": {"type": "STRING"} }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": themes_schema
        }
    }
    
    # Use the existing make_gemini_request function but we will need to re-wrap the result
    # as it assumes a different structure. Instead, we make a more direct call here for simplicity.
    try:
        async with session.post(TEXT_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload)) as response:
            if response.status == 200:
                result = await response.json()
                text_content = result['candidates'][0]['content']['parts'][0]['text']
                print("--- Themes Generator successful. ---")
                return json.loads(text_content)
            else:
                print(f"Themes Generator API Error: {response.status}, {await response.text()}")
                return []
    except Exception as e:
        print(f"Themes Generator Network Error: {e}")
        return []


# --- MODIFIED: Onboarding endpoint now generates themes and saves to DB ---
@app.post("/onboard")
async def create_child_profile(profile: OnboardingProfile):
    """
    Receives profile data, generates personalized themes via Gemini,
    and saves the complete profile to the database.
    """
    # Use model_dump() for Pydantic v2+ to avoid deprecation warnings
    profile_dict = profile.model_dump()
    print("Received /onboard request:", profile_dict)

    # --- Generate Personalized Themes using the new agent ---
    async with aiohttp.ClientSession() as session:
        generated_themes = await themes_generator_agent_llm_call(session, profile_dict)
    
    if not generated_themes or not isinstance(generated_themes, list):
        print("Warning: Failed to generate personalized themes. Storing empty list.")
        generated_themes = []

    themes_as_json_string = json.dumps(generated_themes)

    try:
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO child_profiles (name, age, interests, favorite_activities, autism_severity, communication_level, personalized_themes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (profile.name, profile.age, profile.interests, profile.favoriteActivities, profile.autismSeverity, profile.communicationLevel, themes_as_json_string)
        )
        conn.commit()
        conn.close()
        print("--- Child profile and themes saved successfully to database. ---")
        return {"status": "success", "message": f"Profile for {profile.name} created."}
    except sqlite3.Error as e:
        print(f"Database error on /onboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to save profile to the database.")
# --- MODIFIED: Endpoint to fetch the most recent user's profile ---
@app.get("/profile")
async def get_current_profile():
    """
    Fetches the most recent child profile from the database.
    This eliminates the need for hardcoding the child ID.
    """
    conn = get_db_connection()
    # Get the most recent child profile based on ID (highest ID = most recent)
    profile_row = conn.execute('SELECT * FROM child_profiles ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()

    if profile_row is None:
        raise HTTPException(status_code=404, detail="No child profile found. Please complete onboarding.")

    # Convert to dict and parse personalized_themes JSON
    profile_dict = dict(profile_row)
    try:
        themes_json = profile_dict.get('personalized_themes')
        if themes_json:
            profile_dict['personalized_themes'] = json.loads(themes_json)
        else:
            profile_dict['personalized_themes'] = []
    except (json.JSONDecodeError, TypeError):
        print(f"Warning: Could not parse themes for profile id {profile_dict['id']}.")
        profile_dict['personalized_themes'] = []

    return profile_dict

async def make_gemini_request(session, url, payload, is_json_response=False):
    max_retries = 2
    delay = 1
    headers = {'Content-Type': 'application/json'}

    if is_json_response:
        payload['generationConfig'] = {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "story_part": {"type": "STRING"},
                    "question": {"type": "STRING"},
                    "options": {"type": "ARRAY", "items": {"type": "STRING"}},
                    "image_prompt": {"type": "STRING"}
                },
                "required": ["story_part", "question", "options", "image_prompt"]
            }
        }

    for attempt in range(max_retries):
        try:
            async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
                if response.status == 200:
                    result = await response.json()
                    if not result.get('candidates'):
                        print("API Error: Response is missing 'candidates'. Full response:", result)
                        return None
                    parts = result['candidates'][0]['content']['parts']
                    text_content = parts[0]['text']

                    print("="*80)
                    print("📥 RAW GEMINI API RESPONSE:")
                    print(f"Text length: {len(text_content)} chars")
                    if is_json_response:
                        print("Expected: JSON response")
                        try:
                            parsed = json.loads(text_content)
                            print(f"JSON parsed successfully!")
                            print(f"Keys in response: {parsed.keys() if isinstance(parsed, dict) else 'Not a dict'}")
                            if isinstance(parsed, dict):
                                for key in parsed.keys():
                                    val = parsed[key]
                                    if isinstance(val, str):
                                        print(f"  {key}: {val[:100]}..." if len(val) > 100 else f"  {key}: {val}")
                                    else:
                                        print(f"  {key}: {val}")
                            print("="*80)
                            return parsed
                        except json.JSONDecodeError as e:
                            print(f"❌ JSON PARSE ERROR: {e}")
                            print(f"Raw text: {text_content[:500]}...")
                            print("="*80)
                            return None
                    else:
                        print(f"Text preview: {text_content[:200]}...")
                        print("="*80)
                        return text_content
                else:
                    print(f"API Error: Status {response.status}. Response: {await response.text()}")
                    if response.status == 429:
                        print(f"Rate limited. Retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
                        delay *= 2
                    else:
                        return None
        except aiohttp.ClientError as e:
            print(f"Network Error: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
                delay *= 2
            else:
                print("Max retries reached. Failing.")
                return None
    return None

# --- AGENT FUNCTIONS (API CALLERS) --- (UNCHANGED)

async def planner_agent_llm_call(session, prompt):
    print("--- Calling Planner Agent to generate a story plan... ---")
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response_text = await make_gemini_request(session, TEXT_API_URL, payload)
    print("------------------------------------------------------\n")
    return response_text.strip() if response_text else "A default story about a friendly robot learning to share."

async def story_generator_agent_llm_call(session, prompt):
    print("--- Calling Story Generator Agent for the next part... ---")
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response_json = await make_gemini_request(session, TEXT_API_URL, payload, is_json_response=True)
    print("---------------------------------------------------------\n")
    if response_json:
        return response_json
    else:
        # Fallback
        return {
            "story_part": "Oh no, the storybook page is blank! Let's try this instead: Two friends found a shiny red ball.",
            "question": "What should they do?",
            "options": ["Pick up the ball", "Look for the owner", "Leave the ball"],
            "image_prompt": "Two diverse friends, with surprised expressions, looking at a shiny red ball on green grass. (children's book illustration, simple, vibrant)"
        }

async def image_generator_agent_curl_call(prompt, part_number):
    """
    Makes an asynchronous SUBPROCESS call to your curl command to generate an image.
    --- MODIFIED: Now sends guidance and a negative_prompt ---
    """
    print("--- Calling Image Generator Agent (Cloudflare) to create an illustration... ---")
    
    # --- NEW: Define negative prompt and guidance ---
    # We explicitly forbid the items that appeared by mistake.
    negative_prompt_text = "book, sofa, couch, dog, pet, reading, person on sofa"
    guidance_scale = 10.0  # Force stricter prompt following (default is ~7.5)

    # --- MODIFIED: Create the full payload as a dictionary ---
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt_text,
        "guidance": guidance_scale
    }
    
    # Convert the dictionary to a JSON string for the curl command
    data = json.dumps(payload)
    
    # Define the output filename
    filename = f"story_part_{part_number}.jpg"

    # Build the command arguments list for asyncio.create_subprocess_exec
    cmd_list = [
        "curl",
        "-X", "POST",
        CF_IMAGE_URL,
        "-H", f"Authorization: Bearer {CF_API_TOKEN}",
        "-H", "Content-Type: application/json",
        "--data", data,
        "--output", filename,
        "-s" # Add -s for "silent" mode to hide progress meter
    ]

    try:
        # Create the subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd_list,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the command to complete
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print("--- Curl command successful. ---")
            return filename  # Return the filename on success
        else:
            print(f"--- Curl command failed with code {process.returncode} ---")
            print(f"STDERR: {stderr.decode()}")
            return None

    except Exception as e:
        print(f"Failed to run curl command: {e}")
        return None
    finally:
        print("------------------------------------------------------------------------\n")
# =============================================================================
# TTS ENGINE — edge-tts (all languages) + Gemini TTS (Tanglish primary)
#
# Workflow per language:
#   English   → edge-tts  en-IN-NeerjaNeural
#   Hindi     → edge-tts  hi-IN-SwaraNeural
#   Tamil     → edge-tts  ta-IN-PallaviNeural
#   Tanglish  → (1) try Gemini TTS in parallel with (2) transliterate to Tamil
#               → if Gemini succeeds, use it; otherwise use edge-tts Tamil voice
#   Others    → edge-tts  en-IN-NeerjaNeural  (safe default)
# =============================================================================

EDGE_TTS_VOICES = {
    "english":  "en-IN-NeerjaNeural",   # Female, Indian English
    "hindi":    "hi-IN-SwaraNeural",    # Female, Natural Hindi
    "tamil":    "ta-IN-PallaviNeural",  # Female, Natural Tamil
    "tanglish": "en-IN-PrabhatNeural",  # Male, Indian English (handles Tanglish well)
}

# --- WAV file helper (used by Gemini TTS which outputs raw PCM) ---
def _wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)
    except Exception as e:
        print(f"Error saving WAV file {filename}: {e}")

# --- Gemini TTS (sync, used only for Tanglish primary attempt) ---
def _gemini_tts_sync(text: str, part_number: int) -> str | None:
    """Try Gemini TTS. Returns a .wav filename on success, None on any failure."""
    try:
        g_client = genai.Client()
        response = g_client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=f"say simply and clearly: {text}",
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                    )
                ),
            ),
        )
        parts = response.candidates[0].content.parts
        if not parts or not parts[0].inline_data:
            return None
        filename = f"story_part_{part_number}_audio.wav"
        _wave_file(filename, parts[0].inline_data.data)
        print(f"--- Gemini TTS OK (Part {part_number}) ---")
        return filename
    except Exception as e:
        print(f"--- Gemini TTS failed (Part {part_number}): {e} ---")
        return None

# --- Transliterate Tanglish (romanized Tamil) to Tamil script ---
async def _transliterate_to_tamil(tanglish_text: str) -> str:
    """Convert romanized Tamil text to Tamil script using Google Transliteration.
    Runs the sync HTTP call in a thread so it doesn't block the event loop."""
    try:
        from google.transliteration import transliterate_text
        # transliterate_text uses requests (sync) — run in thread
        result = await asyncio.to_thread(
            lambda: transliterate_text(tanglish_text, lang_code="ta")
        )
        print(f"Transliterated: {tanglish_text[:60]} → {result[:60]}")
        return result
    except Exception as e:
        print(f"Transliteration failed, using original text: {e}")
        return tanglish_text

# --- edge-tts wrapper (natively async) ---
async def _edge_tts_async(text: str, part_number: int, language: str) -> str | None:
    voice = EDGE_TTS_VOICES.get(language.lower(), EDGE_TTS_VOICES["english"])
    filename = f"story_part_{part_number}_audio.mp3"
    print(f"--- Edge TTS Gen (Part {part_number}, voice={voice})... ---")
    start = time.time()
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)
        print(f"--- Edge TTS OK (Part {part_number}) Took: {time.time()-start:.2f}s ---")
        return filename
    except Exception as e:
        print(f"--- Edge TTS FAILED (Part {part_number}): {e} ---")
        return None

# --- Main TTS dispatcher ---
async def generate_tts_audio_async(text: str, part_number: int, language: str = "English") -> str | None:
    lang = language.lower()

    if lang == "tanglish":
        # Run Gemini TTS and Tamil transliteration IN PARALLEL
        print(f"--- TTS: Tanglish detected — trying Gemini + transliteration in parallel (Part {part_number}) ---")
        gemini_task = asyncio.to_thread(_gemini_tts_sync, text, part_number)
        translate_task = _transliterate_to_tamil(text)

        gemini_result, tamil_text = await asyncio.gather(
            gemini_task, translate_task, return_exceptions=True
        )

        if isinstance(gemini_result, str) and gemini_result:
            print(f"✅ Using Gemini TTS for Tanglish Part {part_number}")
            return gemini_result

        # Gemini failed — use Tamil transliteration + edge-tts Tamil voice
        print(f"⚠️ Gemini failed, switching to Edge TTS (Tamil) for Part {part_number}")
        actual_text = tamil_text if isinstance(tamil_text, str) else text
        return await _edge_tts_async(actual_text, part_number, "tamil")

    else:
        # All other languages go directly to edge-tts
        return await _edge_tts_async(text, part_number, lang)

async def generate_one_line_story_plan(session, child_profile, personalized_theme, educational_theme):
    prompt = f"""
    Generate a simple, one-line story plan for a child with the following profile:
    - Name: {child_profile['name']}
    - Age: {child_profile['age']}
    - Interests: {', '.join(child_profile['interests'])}
    - Autism Severity: {child_profile['autism_severity']}
    - Communication Level: {child_profile['communication_level']}

    The story must combine these two themes:
    - Personalized Theme: {personalized_theme}
    - Educational Theme: {educational_theme}

    The plan must be a single, simple sentence that sets up a situation or challenge.
    """
    one_line_plan = await planner_agent_llm_call(session, prompt)
    return one_line_plan

# --- MODIFIED: This function now takes the full history list ---
async def generate_interactive_story_part(session, one_line_plan, story_context_history, child_choice, part_number, language, art_style_guide):
    """
    Generates the story part AND the consistent image prompt at the same time.
    Sends the ENTIRE history of story parts and image prompts for maximum consistency.
    """
    
    # Format the history for the prompt
    formatted_history = ""
    if part_number > 1:
        formatted_history = "Here is the story so far, with each part's corresponding image prompt:\n"
        # Iterate over the list of history dictionaries
        for i, context in enumerate(story_context_history):
            formatted_history += f"--- Part {i+1} ---\n"
            formatted_history += f"Story: \"{context['part']}\"\n"
            formatted_history += f"Image Prompt: \"{context['prompt']}\"\n\n"
    
    # Add language-specific instructions
    language_instruction = ""
    if language.lower() == "tanglish":
        language_instruction = """
    IMPORTANT - Language Format (Tanglish):
    - Write the story in Tamil language BUT use ONLY English alphabet/script (romanized Tamil)
    - Mix Tamil and English words naturally as spoken in everyday conversation
    - Example: "Vanakkam! Leo oru chinna paiyan. Avan romba pudichirundha trains and dinosaurs."
    - Do NOT use Tamil script (வணக்கம்), only romanized Tamil (Vanakkam)
    - Common Tamil words to use (romanized): naan (I), avan/aval (he/she), oru (one/a), romba (very), pudichirundha (liked)
    """
    elif language.lower() == "tamil":
        language_instruction = "\n    Write the story in Tamil using Tamil script (தமிழ்).\n    "
    else:
        language_instruction = f"\n    Write the story in {language}.\n    "
    
    if part_number == 1:
        # Special prompt for the very first part to establish detailed consistency
        prompt = f"""
        You are a storyteller and a meticulous illustrator's assistant for an app for autistic children.
        Your language must be very simple, clear, and encouraging.

        Story Plan: "{one_line_plan}"
        {language_instruction}
        
        --- YOUR TASK (Part {part_number}/5 - INITIAL SCENE) ---
        CRITICAL: Write the "story_part", "question", and ALL "options" in the language specified above. The "image_prompt" should be in English.
        
        First, write a short "story_part" that introduces the main characters and the initial setting based on the story plan.
        
        After writing the story part, do these 3 things:
        1. "question": Ask a simple, forward-looking question that requires the child to make a decision for the story. This must *not* be a comprehension test about what they just read. It must be about what to do *next*.
        2. "options": Provide 3 simple, distinct *actions* that serve as the answers to the "question". Each option must lead the story in a different direction.
        3. "image_prompt": Create a **VERY DETAILED** image prompt for an AI image generator (IN ENGLISH). This prompt is crucial for consistency across the entire story.
            - Start with the **exact** "Art Style" description: "{art_style_guide}".
            - **Describe ALL main characters in detail (appearance, clothing) as they appear in THIS first scene.**
            - **Describe the environment in detail.**
            - Add the main action from the "story_part" you just wrote.
            - This image prompt will be used as a reference for all future images, so be exhaustive.
        
        Your entire response MUST be in the requested JSON format.
        """
    else:
        # For subsequent parts, use the full history for consistency
        prompt = f"""
        You are a storyteller and a meticulous illustrator's assistant for an app for autistic children.
        Your language must be very simple, clear, and encouraging.

        Story Plan: "{one_line_plan}"
        {language_instruction}
        
        --- STORY CONTEXT ---
        The child just made this choice: "{child_choice}"

        --- FULL STORY & IMAGE HISTORY (This is your context) ---
        {formatted_history}
        --- END OF HISTORY ---

        --- IMAGE STYLE GUIDE ---
        **Art Style:** "{art_style_guide}" (You must ALWAYS follow this style)
        
        --- YOUR TASK (Part {part_number}/5) ---
        CRITICAL: Write the "story_part", "question", and ALL "options" in the language specified above. The "image_prompt" should be in English.
        
        First, write a short "story_part" that continues the story based on the child's choice.
        
        After writing the story part, do these 3 things:
        1."question": Ask a simple, forward-looking question that requires the child to make a decision for the story. This must *not* be a comprehension test about what they just read. It must be about what to do *next*.**
        2."options": Provide 3 simple, distinct *actions* that serve as the answers to the "question". Each option must lead the story in a different direction.**
        3.  **"image_prompt"**: Create a NEW, detailed image prompt. This prompt **MUST** be consistent with ALL previous parts.
            a.  Start with the **exact** "Art Style" description: "{art_style_guide}".
            b.  **RE-USE THE EXACT CHARACTER AND ENVIRONMENT DESCRIPTIONS established in the previous parts (especially Part 1).**
            c.  Only update the new action, objects, or small changes relevant to the current "story_part".
        
        Your entire response MUST be in the requested JSON format.
        """
    story_element = await story_generator_agent_llm_call(session, prompt)
    return story_element

# # --- MODIFIED: Main loop now manages a list of history objects ---
# async def main():
#     # 1. Setup
#     child_profile = get_child_profile()
#     personalized_theme = "Dinesh and daniel go on a train adventure"
#     educational_theme = "money management"
#     target_language = "English"
    
#     art_style_guide = "A simple, friendly, and colorful children's book illustration. Use soft, clean lines, vibrant colors, and a happy tone. Avoid scary images, harsh shadows, or complex details."

#     print("--- STORY SETUP ---")
#     print(f"Child: {child_profile['name']}")
#     print(f"Personalized Theme: {personalized_theme}")
#     print(f"Educational Theme: {educational_theme}\n")
    
#     async with aiohttp.ClientSession() as session:
#         # 2. Generate the one-line plan
#         plan = await generate_one_line_story_plan(session, child_profile, personalized_theme, educational_theme)
#         print("--- Generated Story Plan ---")
#         print(plan)
#         print("--------------------------\n")

#         # 3. Iteratively generate the 5-part story
        
#         # --- MODIFIED: This is now a list of dicts to store full context ---
#         story_context_history = [] 
#         user_choice = "Let's begin the story!"

#         for i in range(1, 6):
#             part_number = i
#             print(f"--- Generating Part {part_number}/5 ---")
            
#             time.sleep(1) # Small delay
            
#             # --- MODIFIED: Pass the new history list ---
#             story_part_data = await generate_interactive_story_part(
#                 session, plan, story_context_history, user_choice, part_number, target_language,
#                 art_style_guide
#             )
            
#             print("\n--- Story Segment ---")
#             print(story_part_data["story_part"])
#             print("---------------------\n")
            
#             # (We no longer need the separate full_story_history string)

#             # Get the new prompt generated by Gemini
#             new_image_prompt = story_part_data["image_prompt"]
#             print(f"--- Generated Image Prompt ---\n{new_image_prompt}\n------------------------------\n")

#             # Call the curl function with this new prompt
#             image_filename = await image_generator_agent_curl_call(new_image_prompt, part_number)

#             if image_filename:
#                 print(f"--- Image saved as {image_filename} ---\n")
#             else:
#                 print("--- Could not generate an image for this part. ---\n")

#             # --- CRITICAL: Add the new data to the history list for the next loop ---
#             story_context_history.append({
#                 "part": story_part_data["story_part"],
#                 "prompt": new_image_prompt
#             })
#             # --- END MODIFIED SECTION ---

#             print("--- Interactive Question ---")
#             print(story_part_data["question"])
#             for idx, option in enumerate(story_part_data["options"]):
#                 print(f"{idx + 1}. {option}")
#             print("---------------------------\n")

#             if part_number < 5:
#                 choice_index = -1
#                 while choice_index not in range(len(story_part_data["options"])):
#                     try:
#                         user_input = input(f"Enter your choice (1-{len(story_part_data['options'])}): ")
#                         choice_index = int(user_input) - 1
#                         if choice_index not in range(len(story_part_data["options"])):
#                             print("That's not a valid choice. Please pick a number from the list.")
#                     except ValueError:
#                         print("Please enter a number.")
                
#                 user_choice = story_part_data["options"][choice_index]
#                 print(f"--> You chose: '{user_choice}'\n")
#             else:
#                 print("The story is complete! Well done!")

# if __name__ == "__main__":
#     if not API_KEY or not CF_API_TOKEN or not CF_IMAGE_URL:
#         print("ERROR: Environment variables are not set.")
#         print("Please create a .env file and add your keys, like this:")
#         print('GEMINI_API_KEY="YOUR_GOOGLE_KEY_HERE"')
#         print('CF_API_TOKEN="YOUR_CLOUDFLARE_TOKEN_HERE"')
#         print('CF_IMAGE_URL="YOUR_CLOUDFLARE_WORKER_URL_HERE"')
#     else:
#         try:
#             asyncio.run(main())
#         except KeyboardInterrupt:
#             print("\nStory generation cancelled.")
#---old working---
# @app.post("/start-story")
# async def start_story(request: StoryStartRequest):
#     """
#     Starts a new story. Generates a plan and the first part.
#     """
#     child_profile = get_child_profile()
#     print("Got the request -")
#     print(request)
    
#     async with aiohttp.ClientSession() as session:
#         # 1. Generate the one-line plan
#         plan = await generate_one_line_story_plan(
#             session, child_profile, request.personalized_theme, request.educational_theme
#         )

#         # 2. Generate the first story part
#         story_part_data = await generate_interactive_story_part(
#             session, plan, [], "Let's begin!", 1, request.language, request.art_style_guide
#         )

#         # 3. Generate the image
#         image_prompt = story_part_data["image_prompt"]
#         image_filename = await image_generator_agent_curl_call(image_prompt, 1)

#         image_base64 = None
#         if image_filename and os.path.exists(image_filename):
#             with open(image_filename, "rb") as img_file:
#                 image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
#             os.remove(image_filename) # Clean up the file
       
#         return {
#             "one_line_plan": plan,
#             "story_part_data": story_part_data,
#             "image_base64": image_base64,
#             "part_number": 1
#         }

# @app.post("/continue-story")
# async def continue_story(request: StoryContinueRequest):
#     """
#     Generates the next part of an existing story.
#     """
#     next_part_number = request.part_number + 1
#     async with aiohttp.ClientSession() as session:
#         # 1. Generate the next story part
#         story_part_data = await generate_interactive_story_part(
#             session,
#             request.one_line_plan,
#             request.story_context_history,
#             request.child_choice,
#             next_part_number,
#             request.language,
#             request.art_style_guide
#         )

#         # 2. Generate the image
#         image_prompt = story_part_data["image_prompt"]
#         image_filename = await image_generator_agent_curl_call(image_prompt, next_part_number)

#         image_base64 = None
#         if image_filename and os.path.exists(image_filename):
#             with open(image_filename, "rb") as img_file:
#                 image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
#             os.remove(image_filename) # Clean up the file

#         return {
#             "story_part_data": story_part_data,
#             "image_base64": image_base64,
#             "part_number": next_part_number
        # }
        
#___old working ____


@app.post("/start-story")
async def start_story(request: StoryStartRequest):
    """
    Starts a new story. Generates plan, first part, image, and audio concurrently.
    """
    # Check if Gemini API key was configured successfully at startup
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in environment for /start-story")
        raise HTTPException(status_code=500, detail="Server TTS API Key not configured")

    # Get the most recent child profile from database
    conn = get_db_connection()
    profile_row = conn.execute('SELECT * FROM child_profiles ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()

    if profile_row is None:
        raise HTTPException(status_code=404, detail="No child profile found. Please complete onboarding first.")

    child_profile = dict(profile_row)
    # Parse personalized_themes if needed (though not used in story generation here)
    try:
        themes_json = child_profile.get('personalized_themes')
        if themes_json:
            child_profile['personalized_themes'] = json.loads(themes_json)
        else:
            child_profile['personalized_themes'] = []
    except (json.JSONDecodeError, TypeError):
        child_profile['personalized_themes'] = []
    current_part_num = 1
    print(f"Received /start-story request: {request.dict()}")

    async with aiohttp.ClientSession() as session:
        try:
            # 1. Generate the one-line plan (Sequential)
            plan = await generate_one_line_story_plan(
                session, child_profile, request.personalized_theme, request.educational_theme
            )
            if not plan:
                print("Error: Failed to generate story plan.")
                raise HTTPException(status_code=500, detail="Failed to generate story plan")
            print(f"Generated Plan: {plan}")

            # 2. Generate the first story part (Sequential)
            story_part_data = await generate_interactive_story_part(
                session, plan, [], "Let's begin!", current_part_num, request.language, request.art_style_guide
            )
            if not story_part_data:
                print("Error: Failed to generate story part 1.")
                raise HTTPException(status_code=500, detail="Failed to generate story part 1")

            print("="*80)
            print(f"🎯 STORY PART 1 - DETAILED RESPONSE:")
            print(f"Type: {type(story_part_data)}")
            print(f"Keys: {story_part_data.keys() if isinstance(story_part_data, dict) else 'N/A'}")
            print(f"story_part: {story_part_data.get('story_part', 'MISSING')[:100]}...")
            print(f"question: {story_part_data.get('question', 'MISSING')}")
            print(f"options: {story_part_data.get('options', 'MISSING')}")
            print(f"image_prompt: {story_part_data.get('image_prompt', 'MISSING')[:100]}...")
            print("="*80)

            story_text = story_part_data.get("story_part")
            image_prompt = story_part_data.get("image_prompt")

            if not story_text or not image_prompt:
                print(f"Error: Missing story_part or image_prompt in generated data for part {current_part_num}")
                raise HTTPException(status_code=500, detail="Invalid story data received from text generation")

            # 3. Generate Image and Audio IN PARALLEL
            print(f"--- Starting parallel generation for Part {current_part_num} ---")
            image_task = image_generator_agent_curl_call(image_prompt, current_part_num)
            audio_task = generate_tts_audio_async(story_text, current_part_num, request.language)

            # Wait for both tasks to complete, collect results or exceptions
            results = await asyncio.gather(image_task, audio_task, return_exceptions=True)
            print(f"--- Parallel generation finished for Part {current_part_num} ---")

            # Process results (check for exceptions and get filenames)
            image_filename = None
            audio_filename = None

            if isinstance(results[0], Exception):
                print(f"Error during image generation (Part {current_part_num}): {results[0]}")
                # Optionally raise HTTPException here if image is critical
                # raise HTTPException(status_code=500, detail=f"Failed image generation: {results[0]}")
            elif isinstance(results[0], str):
                image_filename = results[0]
                print(f"Image generation successful: {image_filename}")

            if isinstance(results[1], Exception):
                print(f"Error during audio generation (Part {current_part_num}): {results[1]}")
                # Optionally raise HTTPException here if audio is critical
                # raise HTTPException(status_code=500, detail=f"Failed audio generation: {results[1]}")
            elif isinstance(results[1], str):
                audio_filename = results[1]
                print(f"Audio generation successful: {audio_filename}")

            # 4. Encode results to Base64 and cleanup
            image_base64 = None
            if image_filename and os.path.exists(image_filename):
                try:
                    with open(image_filename, "rb") as img_file:
                        image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                    os.remove(image_filename)
                    print(f"Encoded and removed image file: {image_filename}")
                except Exception as e:
                    print(f"Error processing/removing image file {image_filename}: {e}")
                    # Decide if this error is critical

            audio_base64 = None
            if audio_filename and os.path.exists(audio_filename):
                try:
                    with open(audio_filename, "rb") as aud_file:
                        audio_base64 = base64.b64encode(aud_file.read()).decode('utf-8')
                    os.remove(audio_filename)
                    print(f"Encoded and removed audio file: {audio_filename}")
                except Exception as e:
                    print(f"Error processing/removing audio file {audio_filename}: {e}")
                    # Decide if this error is critical

            # 5. Create tracking session
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO story_sessions (child_id, personalized_theme, educational_theme, language, start_time)
                VALUES (?, ?, ?, ?, datetime('now'))
            """, (child_profile['id'], request.personalized_theme, request.educational_theme, request.language))
            session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            print(f"Created tracking session with ID: {session_id}")

            # 6. Return combined response with session_id
            response = {
                "session_id": session_id,  # NEW: Include session_id for tracking
                "one_line_plan": plan,
                "story_part_data": story_part_data,
                "image_base64": image_base64,
                "audio_base64": audio_base64,
                "part_number": current_part_num
            }

            print("="*80)
            print("📤 FINAL RESPONSE TO FRONTEND:")
            print(f"session_id: {session_id}")
            print(f"part_number: {current_part_num}")
            print(f"story_part_data keys: {response['story_part_data'].keys()}")
            print(f"has image: {image_base64 is not None}")
            print(f"has audio: {audio_base64 is not None}")
            print("="*80)

            return response

        except HTTPException as http_exc:
            # If an error was already raised as HTTPException, just re-raise it
            raise http_exc
        except Exception as e:
            # Catch any other unexpected errors during the process
            print(f"Unexpected error in /start-story: {e}")
            # Return a generic 500 error to the frontend
            raise HTTPException(status_code=500, detail=f"Internal server error during story start: {e}")


@app.post("/continue-story")
async def continue_story(request: StoryContinueRequest):
    """
    Generates the next part of an existing story, including image and audio concurrently.
    """
    # Check if Gemini API key was configured successfully at startup
    if not os.getenv("GOOGLE_API_KEY"): # Simple check
        print("ERROR: GOOGLE_API_KEY not found in environment for /continue-story")
        raise HTTPException(status_code=500, detail="Server TTS API Key not configured")

    current_part_num = request.part_number # The part just completed
    next_part_number = current_part_num + 1
    print(f"Received /continue-story request for Part {next_part_number}: Previous choice='{request.child_choice}'") # Log choice

    async with aiohttp.ClientSession() as session:
        try:
            # 1. Generate the next story part (Sequential)
            story_part_data = await generate_interactive_story_part(
                session, request.one_line_plan, request.story_context_history,
                request.child_choice, next_part_number, request.language, request.art_style_guide
            )
            if not story_part_data:
                print(f"Error: Failed to generate story part {next_part_number}.")
                raise HTTPException(status_code=500, detail=f"Failed to generate story part {next_part_number}")

            print("="*80)
            print(f"🎯 STORY PART {next_part_number} - DETAILED RESPONSE:")
            print(f"Type: {type(story_part_data)}")
            print(f"Keys: {story_part_data.keys() if isinstance(story_part_data, dict) else 'N/A'}")
            print(f"story_part: {story_part_data.get('story_part', 'MISSING')[:100]}...")
            print(f"question: {story_part_data.get('question', 'MISSING')}")
            print(f"options: {story_part_data.get('options', 'MISSING')}")
            print(f"image_prompt: {story_part_data.get('image_prompt', 'MISSING')[:100]}...")
            print("="*80)

            story_text = story_part_data.get("story_part")
            image_prompt = story_part_data.get("image_prompt")

            if not story_text or not image_prompt:
                 print(f"Error: Missing story_part or image_prompt in generated data for part {next_part_number}")
                 raise HTTPException(status_code=500, detail="Invalid story data received from text generation")

            # 2. Generate Image and Audio IN PARALLEL for the *next* part
            print(f"--- Starting parallel generation for Part {next_part_number} ---")
            image_task = image_generator_agent_curl_call(image_prompt, next_part_number)
            audio_task = generate_tts_audio_async(story_text, next_part_number, request.language)

            # Wait for both tasks to complete, collect results or exceptions
            results = await asyncio.gather(image_task, audio_task, return_exceptions=True)
            print(f"--- Parallel generation finished for Part {next_part_number} ---")

            # Process results (check for exceptions and get filenames)
            image_filename = None
            audio_filename = None

            if isinstance(results[0], Exception):
                print(f"Error during image generation (Part {next_part_number}): {results[0]}")
            elif isinstance(results[0], str):
                image_filename = results[0]
                print(f"Image generation successful: {image_filename}")

            if isinstance(results[1], Exception):
                print(f"Error during audio generation (Part {next_part_number}): {results[1]}")
            elif isinstance(results[1], str):
                audio_filename = results[1]
                print(f"Audio generation successful: {audio_filename}")

            # 3. Encode results to Base64 and cleanup
            image_base64 = None
            if image_filename and os.path.exists(image_filename):
                try:
                    with open(image_filename, "rb") as img_file:
                        image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                    os.remove(image_filename)
                    print(f"Encoded and removed image file: {image_filename}")
                except Exception as e:
                    print(f"Error processing/removing image file {image_filename}: {e}")

            audio_base64 = None
            if audio_filename and os.path.exists(audio_filename):
                 try:
                    with open(audio_filename, "rb") as aud_file:
                        audio_base64 = base64.b64encode(aud_file.read()).decode('utf-8')
                    os.remove(audio_filename)
                    print(f"Encoded and removed audio file: {audio_filename}")
                 except Exception as e:
                    print(f"Error processing/removing audio file {audio_filename}: {e}")

            # 4. Return combined response
            response = {
                "story_part_data": story_part_data,
                "image_base64": image_base64,
                "audio_base64": audio_base64,
                "part_number": next_part_number
            }

            print("="*80)
            print("📤 FINAL RESPONSE TO FRONTEND (CONTINUE):")
            print(f"part_number: {next_part_number}")
            print(f"story_part_data keys: {response['story_part_data'].keys()}")
            print(f"story_part_data question: {response['story_part_data'].get('question', 'MISSING')}")
            print(f"story_part_data options: {response['story_part_data'].get('options', 'MISSING')}")
            print(f"has image: {image_base64 is not None}")
            print(f"has audio: {audio_base64 is not None}")
            print("="*80)

            return response
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            print(f"Unexpected error in /continue-story: {e}")
            raise HTTPException(status_code=500, detail=f"Internal server error during story continuation: {e}")

# ============================================
# TRACKING AND ANALYTICS ENDPOINTS
# ============================================

class SessionStartRequest(BaseModel):
    child_id: int
    personalized_theme: str
    educational_theme: str
    language: str

class SessionEndRequest(BaseModel):
    session_id: int
    duration_seconds: int

class ButtonClickRequest(BaseModel):
    session_id: int
    button_type: str
    part_number: int

class AudioReplayRequest(BaseModel):
    session_id: int
    part_number: int

class QuizSubmitRequest(BaseModel):
    session_id: int
    answers: list  # List of dicts: [{"question": str, "correct_answer": str, "user_answer": str}]

@app.post("/api/session/start")
async def start_session(request: SessionStartRequest):
    """Start a new story session for tracking"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO story_sessions (child_id, personalized_theme, educational_theme, language, start_time)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (request.child_id, request.personalized_theme, request.educational_theme, request.language))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {"status": "success", "session_id": session_id}
    except Exception as e:
        print(f"Error starting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/session/{session_id}/end")
async def end_session(session_id: int, request: SessionEndRequest):
    """End a story session and record duration"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE story_sessions
            SET end_time = datetime('now'),
                duration_seconds = ?,
                completed = 1
            WHERE id = ?
        """, (request.duration_seconds, session_id))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Session ended successfully"}
    except Exception as e:
        print(f"Error ending session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tracking/button-click")
async def track_button_click(request: ButtonClickRequest):
    """Track button click events"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO button_clicks (session_id, button_type, part_number, timestamp)
            VALUES (?, ?, ?, datetime('now'))
        """, (request.session_id, request.button_type, request.part_number))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Button click tracked"}
    except Exception as e:
        print(f"Error tracking button click: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tracking/audio-replay")
async def track_audio_replay(request: AudioReplayRequest):
    """Track audio replay events"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audio_replays (session_id, part_number, timestamp)
            VALUES (?, ?, datetime('now'))
        """, (request.session_id, request.part_number))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Audio replay tracked"}
    except Exception as e:
        print(f"Error tracking audio replay: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/quiz/generate")
async def generate_quiz(request: dict):
    """Generate quiz questions based on the completed story"""
    try:
        story_summary = request.get("story_summary", "")
        educational_theme = request.get("educational_theme", "")

        prompt = f"""
        Based on the following story and educational theme, generate 3 simple quiz questions
        that test the child's understanding of the story and the lesson learned.

        Story Summary: {story_summary}
        Educational Theme: {educational_theme}

        Return a JSON array of quiz questions in this format:
        [
          {{
            "question": "What did the character learn?",
            "options": ["option1", "option2", "option3"],
            "correct_answer": "option1"
          }}
        ]
        """

        async with aiohttp.ClientSession() as session:
            quiz_schema = {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "question": {"type": "STRING"},
                        "options": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "correct_answer": {"type": "STRING"}
                    },
                    "required": ["question", "options", "correct_answer"]
                }
            }
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "responseSchema": quiz_schema
                }
            }

            async with session.post(TEXT_API_URL, headers={'Content-Type': 'application/json'},
                                  data=json.dumps(payload)) as response:
                if response.status == 200:
                    result = await response.json()
                    quiz_data = json.loads(result['candidates'][0]['content']['parts'][0]['text'])
                    print(f"✅ Quiz generated: {len(quiz_data)} questions")
                    # Debug: log the structure of the first question so we can see exact field names
                    if quiz_data:
                        print(f"🔍 Quiz question[0] keys: {list(quiz_data[0].keys()) if isinstance(quiz_data[0], dict) else type(quiz_data[0])}")
                        print(f"🔍 Quiz question[0] sample: {quiz_data[0]}")
                    return {"status": "success", "quiz": quiz_data}
                else:
                    error_text = await response.text()
                    print(f"⚠️ Quiz API returned {response.status}: {error_text[:200]}")
                    # Return empty quiz — frontend shows a fallback "Quiz unavailable" message
                    return {"status": "error", "quiz": []}
    except Exception as e:
        print(f"⚠️ Quiz generation failed: {e}")
        # Return empty quiz rather than crashing — frontend handles this gracefully
        return {"status": "error", "quiz": []}

@app.post("/api/quiz/submit")
async def submit_quiz(request: QuizSubmitRequest):
    """Submit quiz answers and calculate score"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        score = 0
        total = len(request.answers)

        for answer in request.answers:
            is_correct = answer["user_answer"] == answer["correct_answer"]
            if is_correct:
                score += 1

            cursor.execute("""
                INSERT INTO quiz_results (session_id, question, correct_answer, user_answer, is_correct, answered_at)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (request.session_id, answer["question"], answer["correct_answer"],
                  answer["user_answer"], is_correct))

        conn.commit()
        conn.close()

        return {
            "status": "success",
            "score": score,
            "total": total,
            "percentage": round((score / total) * 100, 2) if total > 0 else 0
        }
    except Exception as e:
        print(f"Error submitting quiz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}/report")
async def get_session_report(session_id: int):
    """Get comprehensive tracking report for a session"""
    try:
        conn = get_db_connection()

        # Get session data
        session = conn.execute("""
            SELECT s.*, c.name as child_name, c.age
            FROM story_sessions s
            JOIN child_profiles c ON s.child_id = c.id
            WHERE s.id = ?
        """, (session_id,)).fetchone()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Get button clicks
        button_clicks = conn.execute("""
            SELECT button_type, part_number, timestamp, COUNT(*) as count
            FROM button_clicks
            WHERE session_id = ?
            GROUP BY button_type, part_number
            ORDER BY timestamp
        """, (session_id,)).fetchall()

        # Get audio replays
        audio_replays = conn.execute("""
            SELECT part_number, COUNT(*) as replay_count
            FROM audio_replays
            WHERE session_id = ?
            GROUP BY part_number
        """, (session_id,)).fetchall()

        # Get quiz results
        quiz_results = conn.execute("""
            SELECT question, correct_answer, user_answer, is_correct, answered_at
            FROM quiz_results
            WHERE session_id = ?
        """, (session_id,)).fetchall()

        conn.close()

        # Build report
        report = {
            "session_info": dict(session),
            "button_clicks": [dict(row) for row in button_clicks],
            "audio_replays": [dict(row) for row in audio_replays],
            "quiz_results": [dict(row) for row in quiz_results],
            "summary": {
                "total_button_clicks": sum(row[3] for row in button_clicks),
                "total_audio_replays": sum(row[1] for row in audio_replays),
                "quiz_score": sum(1 for row in quiz_results if row[3]) if quiz_results else 0,
                "quiz_total": len(quiz_results) if quiz_results else 0
            }
        }

        # Save report to JSON file
        report_filename = f"session_report_{session_id}.json"
        with open(report_filename, "w") as f:
            json.dump(report, f, indent=2, default=str)

        return {
            "status": "success",
            "report": report,
            "report_file": report_filename
        }
    except Exception as e:
        print(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# SERVE BUILT REACT FRONTEND
# After running `npm run build` inside dream-narrate-web/, FastAPI serves the
# built files so the entire app is accessible on one port (8000).
# Phone/tablet on same WiFi can open http://[laptop-ip]:8000 directly.
# =============================================================================

_DIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dream-narrate-web", "dist")

if os.path.isdir(_DIST_DIR):
    # Serve JS/CSS/image assets
    _assets_dir = os.path.join(_DIST_DIR, "assets")
    if os.path.isdir(_assets_dir):
        app.mount("/assets", StaticFiles(directory=_assets_dir), name="static-assets")

    # Catch-all: return index.html for any path not already handled by an API route.
    # React Router handles client-side navigation from there.
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        return FileResponse(os.path.join(_DIST_DIR, "index.html"))
else:
    print("⚠️  Frontend dist/ not found. Run `npm run build` inside dream-narrate-web/ first.")

# --- Main execution block ---

if __name__ == "__main__":
    if not API_KEY or not CF_API_TOKEN or not CF_IMAGE_URL:
        print("ERROR: Environment variables are not set.")
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)