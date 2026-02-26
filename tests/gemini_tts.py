

# import os
# import io
# import numpy as np
# import sounddevice as sd
# import google.generativeai as genai
# from google.generativeai import types

# # --- Configuration ---

# # 1. API Key (Ensure it's set as an environment variable)
# api_key_configured = False
# try:
#     # Attempt to configure from environment variable first
#     genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
#     print("API Key configured from environment variable.")
#     api_key_configured = True # Flag that configuration was successful
# except KeyError:
#     print("ERROR: GOOGLE_API_KEY environment variable not set.")
#     print("Please set it in your terminal before running the script:")
#     print('  $env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"')
#     # Exit if key is missing
#     # exit("API Key configuration failed.") # Optional: uncomment to stop script if key missing

# # --- REST OF YOUR CONFIGURATION (UNCHANGED) ---
# # 2. Story Text
# story_text = "Hello, Zorp! That train looks like so much fun. Can we please share it?"
# # story_text = "வணக்கம், இது ஒரு சோதனை." # Example Tamil text

# # 3. Voice Selection
# selected_voice_name = 'Kore'
# # selected_voice_name = 'ta-IN-Standard-A' # <-- Replace with actual Tamil voice name if available

# # 4. Audio Playback Configuration
# sample_rate_hertz = 24000
# sample_width_bytes = 2

# # --- End Configuration ---


# def play_gemini_tts(text: str, voice_name: str):
#     """Generates audio using Gemini TTS and plays it back in real-time."""
#     print(f"Synthesizing and playing with voice '{voice_name}': '{text}'...")

#     try:
#         # Get the model instance
#         model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-tts")

#         # Configure the request
#         tts_config = types.GenerateContentConfig(
#             response_modalities=["AUDIO"],
#             speech_config=types.SpeechConfig(
#                 voice_config=types.VoiceConfig(
#                     prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                         voice_name=voice_name,
#                     )
#                 )
#             ),
#         )

#         # Generate content
#         response = model.generate_content(
#             contents=f"Say simply: {text}",
#             generation_config=tts_config
#         )

#         # Extract audio data
#         # --- Check if the response actually contains the expected audio data ---
#         if not response.candidates or not response.candidates[0].content.parts or not response.candidates[0].content.parts[0].inline_data:
#              raise ValueError("Failed to get audio data from Gemini response. Response: " + str(response))
        
#         audio_data_bytes = response.candidates[0].content.parts[0].inline_data.data

#         # --- Playback using sounddevice ---
#         audio_data_np = np.frombuffer(audio_data_bytes, dtype=np.int16)

#         print("Playing audio...")
#         sd.play(audio_data_np, samplerate=sample_rate_hertz, channels=1)
#         sd.wait()
#         print("Playback finished.")

#     except Exception as e:
#         print(f"An error occurred during TTS generation or playback: {e}")
#         # Add more specific error guidance if possible
#         if "API key not valid" in str(e):
#              print("Please check if your GOOGLE_API_KEY is correct.")
#         elif "resource has been exhausted" in str(e):
#              print("You might have hit API rate limits or quota.")
#         elif "Model 'gemini-2.5-flash-preview-tts' not found" in str(e):
#              print("The TTS model name might be incorrect or unavailable.")
#         else:
#             print("General error details:", e)


# # --- Run the function ---
# if __name__ == "__main__":
#     # Use the flag set during configuration
#     if api_key_configured:
#         play_gemini_tts(story_text, selected_voice_name)
#     else:
#         print("API Key not configured. Cannot run TTS.")

from google import genai
from google.genai import types
import wave

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

client = genai.Client()

response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents="இது ஸ்பேஸ் ஸ்கூல்லின் முதல் நாள்! லியோ தன் புதிய நீல யூனிஃபார்மை அணிந்து, பெரிய பிரகாசமான வகுப்பறைக்குள் நடந்தான். திடீரென அவன் ஒரு நண்பனைப் பார்த்தான் — அது பச்சை நிற டைனோசர் ஜார்ப்! ஜார்ப் ஒரு மினுமினுக்கும் சிவப்பு அஸ்ட்ரோ-ட்ரெயினுடன் விளையாடிக் கொண்டிருந்தான், அதை வலுவாகப் பிடித்து கொஞ்சம் பயந்த முகத்துடன் இருந்தான்.",
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
               voice_name='Kore',
            )
         )
      ),
   )
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name='out.wav'
wave_file(file_name, data) # Saves the file to current directory