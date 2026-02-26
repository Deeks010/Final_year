# import os
# import requests
# import base64
# import time
# from dotenv import load_dotenv

# # --- SETUP AND CONFIGURATION ---
# load_dotenv()
# A1_ART_API_KEY = "9517f2a59ca14011ab07221852b094f4"
# # --- PLACEHOLDERS: These must be found on the a1.art website for the specific style/model you want to use ---
# A1_APP_ID = "1838546335502970881" 
# A1_VERSION_ID = "1838546335507165186"
# # This ID corresponds to the overall artistic style filter.
# A1_STYLE_ID = "1838546335507165191" 
# # This is the most critical ID to find. It corresponds to the text prompt input field for your chosen App ID.
# # You may need to inspect the network requests on the a1.art website when using a style to find this value.
# INPUT_ID_FOR_PROMPT = "1838546335507165192" 

# # --- CORRECTED API ENDPOINTS ---
# API_BASE_URL = "https://a1.art/open-api/v1/a1"

# # --- NEW: Function to poll for task results ---
# def poll_for_result(task_id):
#     """
#     Checks the status of a task until it's completed or fails.
#     """
#     polling_url = f"{API_BASE_URL}/tasks/{task_id}"
#     # --- CORRECTED: The header key is 'apiKey' as per new docs ---
#     headers = {"apiKey": A1_ART_API_KEY} 
    
#     for attempt in range(20): # Poll for up to 100 seconds (20 * 5s)
#         try:
#             response = requests.get(polling_url, headers=headers, timeout=10)
#             if response.status_code == 200:
#                 data = response.json()
#                 task_status = data.get('code')
                
#                 if task_status == 0: # 0 means success
#                     task_data = data.get('data', {})
#                     # The 'state' field indicates completion. 10 seems to be the 'completed' state.
#                     if task_data.get('state') == 10:
#                         print("✅ Task completed successfully.")
#                         return task_data
#                     else:
#                         print(f"⏳ Task is still processing (State: {task_data.get('state')})... waiting 5 seconds. (Attempt {attempt + 1}/20)")
#                         time.sleep(5)
#                 else:
#                     print(f"❌ Polling returned an API error code: {task_status}")
#                     print("   Response:", data)
#                     return None
#             else:
#                 print(f"❌ Polling failed with status code {response.status_code}")
#                 print("   Response:", response.text)
#                 return None
#         except requests.exceptions.RequestException as e:
#             print(f"❌ An error occurred during polling: {e}")
#             return None
    
#     print("❌ Task timed out after 100 seconds.")
#     return None

# # --- TEST CASE 1: TEXT-TO-IMAGE GENERATION (Corrected Workflow) ---
# def test_text_to_image():
#     """
#     Tests the text-to-image generation capability using the correct A1.Art API workflow.
#     """
#     print("--- 🧪 Test Case 1: Generating a new image from text... ---")
#     if not A1_ART_API_KEY:
#         print("❌ ERROR: A1_ART_API_KEY is not set in your .env file.")
#         return None

#     prompt = """
#     A simple and friendly children's storybook illustration, colorful with soft, clean lines. 
#     Cartoon style. Cute. Adorable. A small, friendly, green T-Rex with big, curious eyes 
#     and a happy smile, not scary. The T-Rex is standing in a bright, sunny, green valley.
#     """
    
#     # --- CORRECTED: Added the 'styleId' to the payload to fix 'invalid params' error ---
#     payload = {
#         "appId": A1_APP_ID,
#         "versionId": A1_VERSION_ID,
#         "styleId": A1_STYLE_ID,
#         "description": [
#             {
#                 "id": INPUT_ID_FOR_PROMPT,
#                 "value": prompt
#             }
#         ],
#         "size": {
#             "sizeId": "2" # Corresponds to a specific size, e.g., 512x512
#         },
#         "generateNum": 1
#     }
    
#     # --- CORRECTED: Authentication header is 'apiKey' ---
#     headers = {"apiKey": A1_ART_API_KEY, "Content-Type": "application/json"}
    
#     try:
#         # Step 1: Submit the generation task
#         response = requests.post(f"{API_BASE_URL}/images/generate", headers=headers, json=payload, timeout=60)

#         if response.status_code == 200:
#             data = response.json()
#             if data.get('code') == 0 and data.get('data', {}).get('taskId'):
#                 task_id = data['data']['taskId']
#                 print(f"✅ Task submitted successfully. Task ID: {task_id}")
                
#                 # Step 2: Poll for the result
#                 result_data = poll_for_result(task_id)
                
#                 # --- CORRECTED: Parsing the new response structure ---
#                 if result_data and result_data.get('images') and len(result_data.get('images')) > 0:
#                     image_url = result_data['images'][0]
#                     print(f"✅ Image URL received: {image_url}")
                    
#                     # Step 3: Download the image
#                     image_response = requests.get(image_url, timeout=30)
#                     if image_response.status_code == 200:
#                         with open("test_generated_image.png", "wb") as f:
#                             f.write(image_response.content)
#                         print("✅ SUCCESS: Image downloaded and saved as 'test_generated_image.png'")
#                         return "test_generated_image.png"
#                     else:
#                          print(f"❌ FAILED: Could not download image from URL. Status: {image_response.status_code}")
#                 else:
#                     print("❌ FAILED: Did not get a valid image URL from polling result.")
#                     print("   Final Poll Response:", result_data)
#                 return None
#             else:
#                 print("❌ FAILED: API did not return a valid task ID.")
#                 print("   Response:", data)
#                 return None
#         else:
#             print(f"❌ FAILED: API returned status code {response.status_code}")
#             print("   Response:", response.text)
#             return None
            
#     except requests.exceptions.RequestException as e:
#         print(f"❌ FAILED: An error occurred during the request: {e}")
#         return None

# # --- TEST CASE 2: IMAGE-TO-IMAGE EDITING ---
# def test_image_to_image(generated_image_path):
#     """
#     Demonstrates the likely structure for an image-to-image API call based on new docs.
#     """
#     print("\n--- 🧪 Test Case 2: Editing an existing image (Demonstration)... ---")
    
#     if not generated_image_path or not os.path.exists(generated_image_path):
#         print("❌ ERROR: Valid image path not provided. Run Test Case 1 first.")
#         return

#     print("⚠️ NOTE: The image-to-image API requires uploading an image first to get a URL and path.")
#     print("   This test will demonstrate the payload structure but will not make a live API call.")

#     edit_prompt = "A small, friendly, green T-Rex is now WAVING."

#     # The 'cnet' field is used for image-to-image. You need IDs and paths for this,
#     # which you would get from their web UI or a separate upload API if they provide one.
#     payload = {
#         "appId": A1_APP_ID,
#         "versionId": A1_VERSION_ID,
#         "styleId": A1_STYLE_ID,
#         "description": [
#             {"id": INPUT_ID_FOR_PROMPT, "value": edit_prompt}
#         ],
#         "size": {"sizeId": "2"},
#         "generateNum": 1,
#         "cnet": [
#             {
#                 "id": "PLACEHOLDER_CNET_ID", # You must find this ID from the app's form on a1.art
#                 "imageUrl": "https://example.com/your-uploaded-image.png", # URL of your uploaded source image
#                 "path": "PLACEHOLDER_PATH" # Path from an image upload response
#             }
#         ]
#     }
    
#     print("\n--- Payload that WOULD be sent for Image-to-Image: ---")
#     import json
#     print(json.dumps(payload, indent=2))

# # --- MAIN EXECUTION ---
# if __name__ == "__main__":
#     print("Starting A1.Art API tests...")
#     # Run the first test to generate the base image
#     generated_file = test_text_to_image()
#     if generated_file:
#         # If the first test succeeds, demonstrate the editing structure
#         test_image_to_image(generated_file)



import os
import requests
from dotenv import load_dotenv

load_dotenv()

# --- 1. YOUR DETAILS ---
API_KEY = os.environ.get("A1ART_API_KEY")  # Set A1ART_API_KEY in your .env file
# -----------------------



LIST_APPS_URL = 'https://a1.art/api/v1/app/list'

def find_available_apps():
    print("Fetching list of available apps from a1.art...")
    
    headers = {
        'apiKey': API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {} 

    try:
        # We've added a 10-second timeout to stop it from hanging
        response = requests.post(
            LIST_APPS_URL, 
            headers=headers, 
            json=payload, 
            timeout=10  # <--- NEW: Give up after 10 seconds
        )
        response.raise_for_status() 
        
        data = response.json()
        
        if data.get('code') != '000000':
            raise Exception(f"API Error: {data.get('message')}")
        
        apps = data['data']['list']
        
        if not apps:
            print("No apps were found. Your API key might not have permissions.")
            return

        print(f"\n--- Found {len(apps)} Available Apps (Showing first 10) ---")
        
        # We are slicing the list to only loop over the first 10 items
        for app in apps[:10]: # <--- NEW: Only get the first 10 from the list
            app_id = app.get('id')
            version_id = app.get('versionId')
            app_name = app.get('name', 'Unnamed App')
            
            prompt_id = None
            if app.get('formArr'):
                for form_item in app['formArr']:
                    if form_item.get('type') == 'description' and form_item.get('inputs'):
                        prompt_id = form_item['inputs'][0].get('id')
                        break
            
            if not prompt_id:
                prompt_id = "N/A (This app may not use a text prompt)"

            print("---------------------------------")
            print(f"App Name: {app_name}")
            print(f"   appId: {app_id}")
            print(f"   versionId: {version_id}")
            print(f"   prompt_id: {prompt_id}")
            print("---------------------------------")
            
        print("\nACTION: Choose an app from this list.")
        print("Copy its 'appId', 'versionId', and 'prompt_id' into the main test file.")

    except requests.exceptions.Timeout:
        print("\n--- ERROR: The request timed out. ---")
        print("This almost always means a FIREWALL, ANTIVIRUS, or VPN is blocking Python.")
        print("Please check your security software and allow this script to access the internet.")
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    find_available_apps()