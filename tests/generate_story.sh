#!/bin/bash

# --- Configuration ---
# 👇 !! REPLACE THIS WITH YOUR REAL TOKEN !! 👇
API_TOKEN="12345678" 
API_URL="https://story-image-generation.221501028.workers.dev/"
OUTPUT_DIR="story_images"
# --- End Configuration ---

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Starting story generation... Images will be saved to $OUTPUT_DIR/"

# --- Image 1: The Setup ---
echo "Generating Image 1: The Setup..."
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"prompt": "Maya, a 7-year-old girl with brown braided hair, wearing a bright red jacket and blue jeans, is walking alone on a cobblestone path in a sunny autumn park. The park has large oak trees with orange and yellow leaves and a distinct green wooden bench in the background. (children'\''s book illustration, digital art, vibrant colors)"}' \
  --output "$OUTPUT_DIR/story_1.jpg"

# --- Image 2: The Discovery ---
echo "Generating Image 2: The Discovery..."
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"prompt": "In the same sunny autumn park with oak trees, Maya (7-year-old girl, brown braided hair, red jacket, blue jeans) kneels on the cobblestone path. She looks surprised as she spots a small, scruffy golden retriever puppy with a blue collar hiding behind the green wooden bench. (children'\''s book illustration, digital art, vibrant colors)"}' \
  --output "$OUTPUT_DIR/story_2.jpg"

# --- Image 3: The Connection ---
echo "Generating Image 3: The Connection..."
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"prompt": "Close-up shot in the same autumn park. Maya (7-year-old girl, brown braided hair, red jacket) is sitting on the green grass, gently petting the small, scruffy golden retriever puppy (blue collar). The puppy is wagging its tail and licking her hand. The green wooden bench is visible behind them. (children'\''s book illustration, digital art, vibrant colors)"}' \
  --output "$OUTPUT_DIR/story_3.jpg"

# --- Image 4: The Journey Home ---
echo "Generating Image 4: The Journey Home..."
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"prompt": "Maya (7-year-old girl, brown braided hair, red jacket) is walking on the cobblestone path, leaving the autumn park. She is carefully holding the small, scruffy golden retriever puppy (blue collar) in her arms. The park'\''s oak trees and green bench are in the distance. (children'\''s book illustration, digital art, vibrant colors)"}' \
  --output "$OUTPUT_DIR/story_4.jpg"

# --- Image 5: The New Home ---
echo "Generating Image 5: The New Home..."
curl -X POST "$API_URL" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"prompt": "Inside a cozy living room, Maya (7-year-old girl, brown braided hair, red jacket) is sitting on a beige carpet. She is giving a bowl of water to the small, scruffy golden retriever puppy (blue collar), who is happily drinking. A fireplace and a sofa are in the background. (children'\''s book illustration, digital art, vibrant colors)"}' \
  --output "$OUTPUT_DIR/story_5.jpg"

echo "✅ All 5 images generated successfully in $OUTPUT_DIR/"