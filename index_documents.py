import os
import psycopg2
import google.generativeai as genai  
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document

# Load environment variables from the .env file
load_dotenv()

# Retrieving the keys
DB_URL = os.getenv("POSTGRES_URL")
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if keys are loaded correctly
if not DB_URL or not GOOGLE_API_KEY:
    print("Error: Keys not found. Make sure .env file exists and contains POSTGRES_URL and GEMINI_API_KEY.")
    exit()

# Configuring the AI
genai.configure(api_key=GOOGLE_API_KEY)

# Reads the content of a PDF or DOCX file and returns the raw text string
def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif ext == '.docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Splits the long text into smaller segments (chunks) with a specific overlap
def chunk_text(text, chunk_size=1000, overlap=200):
    # Splitting by fix size
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

# Generates a vector embedding for the given text using Google's Gemini model
def get_embedding(text):
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Embedding Error: {e}")
        return None

# Saves the text chunks and their corresponding embeddings into the Postgres database
def save_to_db(chunks, embeddings, filename):
    # Saving to Neon database
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        insert_query = """
        INSERT INTO document_chunks (chunk_text, embedding, filename, split_strategy)
        VALUES (%s, %s, %s, %s)
        """
        
        for chunk, vector in zip(chunks, embeddings):
            # Using list(vector) to ensure compatibility
            cur.execute(insert_query, (chunk, list(vector), filename, 'fixed-size'))
            
        conn.commit()
        cur.close()
        conn.close()
        print(f"SUCCESS! Saved {len(chunks)} chunks to the database.")
    except Exception as e:
        print(f"Database Error: {e}")

# Main execution block
if __name__ == "__main__":
    file_name = "Warranty_Certificate.pdf" 
    
    if not os.path.exists(file_name):
        print(f"Please put a file named '{file_name}' in the folder!")
    else:
        print("1. Extracting text...")
        text = extract_text_from_file(file_name)
        
        if text:
            print("2. Chunking text...")
            chunks = chunk_text(text)
            
            print("3. Generating embeddings (this might take a moment)...")
            embeddings = []
            for chunk in chunks:
                emb = get_embedding(chunk)
                if emb:
                    embeddings.append(emb)
            
            print("4. Saving to Neon DB...")
            save_to_db(chunks, embeddings, file_name)