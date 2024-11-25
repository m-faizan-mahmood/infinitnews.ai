import requests
from PIL import Image
import io
import pandas as pd
import os

# API Configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large-turbo"
headers = {
    "Authorization": "Bearer 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"  # Replace HF_TOKEN with your actual Hugging Face token
}

# Function to query the API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Read the CSV file
csv_path = "/content/output_90020241125_060001.csv"
df = pd.read_csv(csv_path)

# Check if the 'ai_gen_title' column exists
if 'gan_prompts' not in df.columns:
    raise ValueError("The column 'gan_prompts' does not exist in the CSV file.")

# Limit processing to the first three rows
titles = df['gan_prompts'].head(3)

# Directory to save images
output_dir = "/content/generated_images"
os.makedirs(output_dir, exist_ok=True)

# Iterate over the first three titles and generate images
for index, title in enumerate(titles):
    print(f"Processing: {title} ({index + 1}/3)")
    payload = {"inputs": title}
    image_bytes = query(payload)

    if image_bytes:
        try:
            # Create the image
            image = Image.open(io.BytesIO(image_bytes))
            # Save the image with a unique name
            filename = os.path.join(output_dir, f"image_6{index + 1}.png")
            image.save(filename)
            print(f"Image saved: {filename}")
        except Exception as e:
            print(f"Error processing title '{title}': {e}")

print("Images for the first three rows processed and saved.")
