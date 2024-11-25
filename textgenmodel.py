import os
import pandas as pd
import re
import logging
import pyttsx3
import os
import logging
from datetime import datetime
from gtts import gTTS
from groq import Groq
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("automation.log"), logging.StreamHandler()],
)

# Set the API key as an environment variable
os.environ["GROQ_API_KEY"] = "--"  # Replace with your actual API key

# Initialize Groq client
client = Groq()

# Paths
DATASET_PATH = "/content/9ai_article_details.csv"
OUTPUT_PATH = f"/content/output_900{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
AUDIO_OUTPUT_DIR = "/content/audio_files/new/1audio_files"

# Ensure the audio output directory exists
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

# Regex pattern for extracting titles
TITLE_PATTERN = r"^\*\*(.+?)\*\*"

# Groq API helpers
def generate_news_speech(article):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a news anchor for InfinitNews preparing for a live broadcast. "
                        "Your task is to create a concise, clear, and engaging summary based on the following article. "
                        "always start with Good evening, and welcome to InfinitNews, The speech should focus on the key points, delivering accurate and factual information in a way that captures the audience’s attention. "
                        "Maintain a formal yet lively tone with smooth transitions between points, as if presenting live on air. "
                        "Keep the language simple and avoid technical jargon, ensuring the content is accessible to a wide audience. "
                        "Your goal is to deliver a polished, professional, and informative segment that is both engaging and easy to follow. give the whole news under 150 characters"
                    ),
                },
                {"role": "user", "content": article},
            ],
            temperature=0.8,
            max_tokens=300,
            top_p=0.9,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating speech: {e}")
        return None

def generate_article(content):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Adjust model name if needed
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Act as a psychological expert, seo expert & news article writer use a informative tone. Your task is to humanize and enhance "
                        "the provided news article by presenting a clear while incorporating key "
                        "details and insights. Ensure the explanation is objective, accurate, and provides a broader "
                        "understanding of the topic make it persuasive and Focus on presenting the news in an engaging yet professional manner ,make sure its not recognized as a ai written article"
                        "write in a format that the important information is clearly stated in the starting, use such a tone to lure in the reader strategically and "
                        "in a way that persuades the reader. Wherever possible, Give a seo optimized clear and compelling title thats formal and persuasades the reader "
                        "cite multiple sources to back up key points, include all the backlinks, and ensure accuracy. write more then 2000 words "
                        "in the end give a disclaimer that this content is AI-Generated News Powered by infinitdigitals.io Strictly for Research Purposes."
                    ),
                },
                {"role": "user", "content": content},
            ],
            temperature=0.7,
            max_tokens=2500,
            top_p=1,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating article: {e}")
        return None

def generate_prompt(article):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Adjust model name if needed
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI prompt engineer specializing in crafting highly descriptive prompts for GAN image generation. "
                        "Based on the given article, create a prompt that includes setting, style (e.g., realism, Surrealism, imaginative,), mood, objects, aestheticness, set the scenery like premium cinematic film "
                        "characters, colors, and artistic influences. Ensure the description inspires unique, visually engaging, ensure the aestheticness , and relevence and high-quality images using detailed description. "
                        "Do not repeat the title verbatim; use it as inspiration to craft a visually compelling prompt description & dont include any disclaimer example :: Here's a prompt that captures the essence of the article or any disclaimerother in starting, middle or end"
                    ),
                },
                {"role": "user", "content": article},
            ],
            temperature=0.8,
            max_tokens=300,
            top_p=0.9,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating prompt: {e}")
        return None

# Updated TTS Function using gTTS
def generate_audio(text, index):
    try:
        if not text or pd.isna(text):
            return None
        file_name = f"news_speech_{index + 1}.mp3"
        audio_path = os.path.join(AUDIO_OUTPUT_DIR, file_name)
        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)
        logging.info(f"Audio file saved at: {audio_path}")
        return audio_path
    except Exception as e:
        logging.error(f"Error generating audio for index {index}: {e}")
        return None


# Utility functions
def extract_title(text):
    if pd.isna(text):
        return None
    match = re.search(TITLE_PATTERN, text, re.MULTILINE)
    return match.group(1) if match else None

def process_in_parallel(data, func):
    results = [None] * len(data)
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_index = {executor.submit(func, item): idx for idx, item in enumerate(data)}
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                logging.error(f"Error processing item at index {idx}: {e}")
    return results

def text_to_speech(text, filename):
    try:
        # Initialize TTS engine within the function
        tts_engine = pyttsx3.init()
        tts_engine.save_to_file(text, filename)
        tts_engine.runAndWait()
        logging.info(f"TTS saved to {filename}")
    except Exception as e:
        logging.error(f"Error during TTS conversion: {e}")


# Main Automation Function
def automate_pipeline(dataset_path, output_path):
    try:
        # Load dataset
        logging.info("Loading dataset...")
        df = pd.read_csv(dataset_path)

        # Generate AI articles
        logging.info("Generating AI articles...")
        df["ai_gen_articles"] = process_in_parallel(df["content"].tolist(), generate_article)

        # Extract titles
        logging.info("Extracting titles...")
        df["ai_gen_title"] = df["ai_gen_articles"].apply(extract_title)

        # Generate GAN prompts
        logging.info("Generating GAN prompts...")
        df["gan_prompts"] = process_in_parallel(df["ai_gen_title"].tolist(), generate_prompt)

        # Generate news anchor speeches
        logging.info("Generating news speeches...")
        df["news_speech"] = process_in_parallel(df["ai_gen_articles"].tolist(), generate_news_speech)

        # Convert news speeches to audio files
        logging.info("Converting news speeches to audio...")
        df["audio_path"] = process_in_parallel(
            [(text, idx) for idx, text in enumerate(df["news_speech"].tolist())],
            lambda x: generate_audio(x[0], x[1])
        )

        # Save results
        df.to_csv(output_path, index=False)
        logging.info(f"Pipeline completed. Results saved to {output_path}")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")


        # Save results
        df.to_csv(output_path, index=False)
        logging.info(f"Pipeline completed. Results saved to {output_path}")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

# Run the pipeline
automate_pipeline(DATASET_PATH, OUTPUT_PATH)
