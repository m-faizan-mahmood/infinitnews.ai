
# INFINITNEWS.AI Automation Pipeline for Text, Image, and Audio Generation

## Overview

The **AI Automation Pipeline** is a comprehensive, end-to-end solution designed to automate the generation of content in multiple formats, including text, images, and audio.
This pipeline integrates various advanced AI technologies for text generation, image synthesis, and audio conversion. By leveraging cutting-edge tools such as **Groq**,
**Hugging Face**, and **Google Text-to-Speech (gTTS)**, the pipeline aims to streamline content creation processes for use cases in digital media, news generation, and content marketing.

## Key Features

- **Data Scraping**: Automates the extraction of raw article data from CSV files or external sources, preparing it for AI processing.
- **Text Generation**: Utilizes the **Groq** AI model to generate high-quality, relevant, and engaging articles from input content.
- **Image Generation**: Uses **Hugging Face's Stable Diffusion API** to create visually appealing images based on AI-generated text prompts.
- **Audio Generation**: Converts the generated text content into lifelike audio using **Google Text-to-Speech (gTTS)**, enabling use cases such as podcasts or voice-driven applications.

## Folder Structure

```plaintext
/content
├── audio_files          # Generated audio files (MP3)
├── generated_images     # Generated images (PNG)
└── output_data.csv      # CSV file containing generated text, image, and audio metadata
```

## Prerequisites

Before running the pipeline, ensure that you have the following:

- **Python 3.x**
- **Required Libraries**:
    - `requests`
    - `pandas`
    - `gTTS`
    - `pyttsx3`
    - `PIL`
    - `groq`
    - `os`
    - `io`
    - `logging`
    - `concurrent.futures`

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone this repository:

```bash
git clone https://github.com/your-username/ai-automation-pipeline.git
```

2. Set up your environment variables, particularly for the API keys:

```bash
export HF_API_KEY="your_huggingface_api_key"
export GROQ_API_KEY="your_groq_api_key"
```

## How It Works

### 1. **Data Scraping**
The pipeline starts by reading and processing a CSV file containing article data. The script scrapes relevant content and formats it for further processing by AI models.

### 2. **Text Generation**
Once the data is prepared, the **Groq API** is used to generate high-quality, human-like articles based on the content. The generated text can be news articles, summaries, or other types of content.

### 3. **Image Generation**
Using **Hugging Face's Stable Diffusion API**, the pipeline generates images related to the text prompts. These images are saved locally and associated with the generated content, enhancing the visual appeal of the articles.

### 4. **Audio Generation**
Finally, the generated text is converted into audio using **Google Text-to-Speech (gTTS)**. The resulting audio files are saved in the `/audio_files` directory and can be used for podcasts, news broadcasts, or other media applications.

## Usage

To run the entire pipeline, simply execute the following script:

```bash
python automate_pipeline.py
```

This command will trigger the full pipeline, processing the CSV input and generating the following:

- **AI-generated articles**
- **Image files** corresponding to each article
- **Audio files** for each article in MP3 format

The output will be saved in the `generated_images` and `audio_files` directories, while metadata about the generated content (e.g., image paths, audio paths) will be stored in `output_data.csv`.

## Output

The pipeline generates the following outputs:

- **CSV File (`output_data.csv`)**: This file contains metadata for each generated article, including:
    - AI-generated article text
    - Corresponding image and audio paths
    - GAN prompts used for image generation

- **Audio Files (`audio_files/`)**: The text-based articles are converted into audio using **gTTS**. These files are saved as `.mp3` files.

- **Image Files (`generated_images/`)**: Images corresponding to the text prompts are generated using **Stable Diffusion** and saved as `.png` files.

### Example Output (CSV)

| ai_gen_articles    | ai_gen_title       | gan_prompts         | news_speech   | audio_path        | image_path  |
|--------------------|--------------------|---------------------|---------------|-------------------|-------------|
| Article 1 Content  | Article 1 Title    | Prompt 1            | Speech 1 Text | /audio/1.mp3      | /image/1.png|
| Article 2 Content  | Article 2 Title    | Prompt 2            | Speech 2 Text | /audio/2.mp3      | /image/2.png|
| ...                | ...                | ...                 | ...           | ...               | ...         |

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! If you have ideas for improving this project or adding new features, feel free to submit a pull request or open an issue.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push the changes to your fork (`git push origin feature/your-feature`).
5. Create a pull request.

## Acknowledgements

- **Hugging Face** for providing access to state-of-the-art models for text and image generation.
- **Groq** for offering powerful AI-driven content generation tools.
- **Google Text-to-Speech (gTTS)** for enabling high-quality audio conversion from text.

---

### Final Thoughts

This **AI Automation Pipeline** leverages advanced AI technologies to automate the process of content creation and distribution. By combining text generation, image creation, and audio conversion, this pipeline can be a valuable tool for businesses, content creators, and digital marketers looking to streamline their content production workflow. Whether for generating news articles, blogs, or multimedia content, this project offers an efficient and scalable solution.
