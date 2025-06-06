# RAG based Docuemnt Management System

## Overview
This project processes and indexes text documents using FAISS for efficient similarity search. It supports embedding entire documents and individual sentences for fine-grained search queries about specific information on any document.

## Features
- Detects file encoding and extracts text from PDFs and other text files.
- Cleans and tokenizes text into sentences.
- Generates and stores embeddings for documents and sentences.
- Uses FAISS for efficient similarity searches.
- Stores document metadata and embeddings in SQLite.

## Setup Instructions
### Prerequisites
- Python 3.10+
- NOTE: this uses the faiss-gpu package, which may not work if you have a gpu that doesnt support CUDA. Consider switching to the faiss-cpu package instead.
### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```
2. Install dependencies:
   ```sh
   make install-all
   ```

## Usage
### 1. Parsing a Document
Use `parse_doc(file_path)` to extract and clean text from a document.

### 2. Saving Embeddings
Call `save_embedding(doc_id, doc_name, embedding, text, sentence_embeddings)` to store document embeddings in the database and FAISS index.

### 3. Querying for Similar Documents
Use FAISS to search for similar documents:
```python
query_embedding = model.encode("your query text")
D, I = doc_index.search(query_embedding.reshape(1, -1), k=5)
```

## Running the Project Locally

### Running the Backend
1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Start the backend server:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload  
   ```
   OR
1. Run with the make file:
    ```sh
   make run-backend
    ```
### Running the Frontend
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Build the frontend:
   ```sh
   npm run build
   ```
3. Preview the frontend:
   ```sh
   npm run preview
   ```
### Running both at the same time (requires you to build the frontend first )
1. In the root directory, run:
   ```sh
   make start
   ```