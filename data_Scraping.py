import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import threading

# Base URL of the website
base_url = "https://tribune.com.pk/latest"

# Function to extract articles from a single page
def extract_articles(page_url):
    try:
        response = requests.get(page_url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all articles with their links and titles
        articles = []
        for item in soup.find_all('h2', class_='title-heading add-mrgn-top lh-mb'):
            title = item.get_text(strip=True)
            link = item.find_previous('a', href=True)['href'] if item.find_previous('a', href=True) else "Link not found"
            articles.append({'name': title, 'article site': link})

        return articles

    except Exception as e:
        print(f"Error extracting articles: {e}")
        return []

# Function to save articles into a CSV file
def save_to_csv(articles, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'article site']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:  # Write header if the file is empty
            writer.writeheader()
        writer.writerows(articles)

# Function to extract details from a single article
def extract_article_details(url):
    try:
        # Send a GET request to the article URL
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the headline
        headline = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Headline not found"

        # Extract the publication date (only the date part)
        date = soup.find('div', {'class': 'left-authorbox'}).find_all('span')[-1].get_text(strip=True) if soup.find('div', {'class': 'left-authorbox'}) else "Date not found"

        # Extract the main content of the article
        content = " ".join([p.get_text(strip=True) for p in soup.find_all('p')]) if soup.find_all('p') else "Content not found"

        return {'url': url, 'headline': headline, 'date': date, 'content': content}

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return {'url': url, 'headline': "Error", 'date': "Error", 'content': "Error"}

# Function to process each URL from the CSV file
def process_articles_from_csv(input_csv, output_csv, processed_urls):
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        urls = [row['article site'] for row in reader if row['article site'] not in processed_urls]

    # For each URL, extract details, save them, and update the processed URLs
    for url in urls:
        print(f"Processing article: {url}")
        article_details = extract_article_details(url)
        
        # Save the article details in the output CSV
        with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['url', 'headline', 'date', 'content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.path.getsize(output_csv) == 0:  # Check if file is empty, if so write header
                writer.writeheader()
            writer.writerow(article_details)

        # Mark this URL as processed
        processed_urls.add(url)

        # Wait a moment before processing the next article (optional)
        time.sleep(2)  # Sleep for 2 seconds between article processing to avoid hitting the server too hard

# Function to continuously fetch new articles and immediately process each one
def continuously_fetch_data(base_url, input_csv, output_csv, processed_urls):
    while True:
        print(f"Checking for new articles at: {base_url}")
        articles = extract_articles(base_url)

        # Deduplicate articles
        new_articles = [article for article in articles if article['article site'] not in processed_urls]

        if new_articles:
            print(f"Found {len(new_articles)} new articles. Saving to {input_csv}")
            save_to_csv(new_articles, input_csv)

            # Process the articles from the CSV file and save their details
            process_articles_from_csv(input_csv, output_csv, processed_urls)
        else:
            print("No new articles found. Retrying after a delay.")

        # Sleep for a bit before checking for new articles
        time.sleep(60)  # Wait for 60 seconds before scraping again

# Initialize a set to keep track of processed URLs
processed_urls = set()


# CSV file paths
input_csv = "/content/infinitnews.ai/output/tribune_scraped_data/9tribune_articlesauto.csv"  # Input CSV path
output_csv = "/content/infinitnews.ai/output/tribune_scraped_data/9ai_article_details.csv"  # Output CSV path

# Start the article scraping and processing tasks in parallel using threading
scraping_thread = threading.Thread(target=continuously_fetch_data, args=(base_url, input_csv, output_csv, processed_urls))
scraping_thread.start()

# Join threads to keep the main program running
scraping_thread.join()
