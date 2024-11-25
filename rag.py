import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline
import gradio as gr

# Load and preprocess the dataset
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['content'] = df['content'].fillna('').str.strip()
    df['headline'] = df['headline'].fillna('').str.strip()
    return df

# Generate embeddings and create a FAISS index
def create_embeddings_and_index(df, model_name='all-MiniLM-L6-v2'):
    # Load the embedding model
    model = SentenceTransformer(model_name)
    
    # Generate embeddings for content
    embeddings = model.encode(df['content'].tolist(), show_progress_bar=True)
    np.save('embeddings.npy', embeddings)  # Save embeddings for later use
    
    # Create and populate the FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, 'news_index.faiss')  # Save the FAISS index
    
    return model, index

# Search function
def search(query, model, index, df, top_k=5):
    try:
        query_embedding = model.encode([query])
        distances, indices = index.search(query_embedding, top_k)
        results = []
        for idx in indices[0]:
            results.append(df.iloc[idx])
        return results
    except Exception as e:
        return f"Error during search: {e}"

# Retrieval-Augmented Generation pipeline
def rag_pipeline(query, model, index, df, summarizer, top_k=5):
    retrieved_articles = search(query, model, index, df, top_k)
    if isinstance(retrieved_articles, str):  # Handle search errors
        return retrieved_articles

    summaries = []
    for article in retrieved_articles:
        try:
            summary = summarizer(article['content'], max_length=100, min_length=30, do_sample=False)
            summaries.append((article['headline'], summary[0]['summary_text']))
        except Exception as e:
            summaries.append((article['headline'], f"Error summarizing content: {e}"))
    return summaries

# Main function to execute all steps
def main():
    # File path to the dataset
    file_path = '/content/infinitnews.ai/output/tribune_scraped_data/9ai_article_details.csv'
    
    # Load and preprocess the data
    df = load_and_preprocess_data(file_path)
    
    # Create embeddings and FAISS index
    model, index = create_embeddings_and_index(df)
    
    # Load summarization model
    summarizer = pipeline('summarization')

    # Build Gradio interface
    def query_interface(user_query):
        results = rag_pipeline(user_query, model, index, df, summarizer)
        return {headline: summary for headline, summary in results}

    iface = gr.Interface(
        fn=query_interface,
        inputs=gr.Textbox(label="Enter your query"),
        outputs=gr.JSON(label="Relevant Summaries"),
        title="Robust RAG Application"
    )
    iface.launch()

# Execute the main function
if __name__ == "__main__":
    main()
