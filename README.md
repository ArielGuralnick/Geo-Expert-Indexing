# Geo-Expert Document Indexing Module

A Python module developed as part of a home assignment for Jeen.ai.
The script performs a complete processing cycle for vehicle documents (supporting PDF/DOCX). Currently, it processes a warranty certificate by extracting text, splitting it into segments (chunking), generating embeddings using the **Gemini API**, and storing them in a **PostgreSQL** database.

## Prerequisites

- Python 3.9+
- PostgreSQL Database (Neon.tech recommended)
- Google Gemini API Key

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/ArielGuralnick/Geo-Expert-Indexing](https://github.com/ArielGuralnick/Geo-Expert-Indexing)
    ```

2.  **Install required packages:**

    ```bash
    pip install google-generativeai psycopg2-binary python-dotenv pypdf python-docx cryptography
    ```

3.  **Configuration (Security & Environment Variables):**

    > **Note:** For security reasons, API keys are not stored in the repository.

    To run this project, you need to set up your own environment variables:

    1.  Locate the `.env.example` file in the root directory.
    2.  Create a copy of this file and name it `.env` (this file is git-ignored).
    3.  Open the new `.env` file and fill in your credentials:
        - `GEMINI_API_KEY`: Your API key from Google AI Studio.
        - `POSTGRES_URL`: Your connection string for the PostgreSQL database.

## Usage

To run the indexing process, ensure a file named `Warranty_Certificate.pdf` exists in the project folder, then execute:

```bash
python index_documents.py
```

## Chunking Strategy

This project utilizes a Fixed-size with overlap strategy. This ensures semantic continuity between different text segments and improves retrieval accuracy by maintaining context across chunk boundaries.
