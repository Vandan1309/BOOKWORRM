# BOOKWORRM# BOOKWORRM — Your AI-Assisted Bookmark

**Stay curious. Go beyond the page.**

BOOKWORRM is an AI-powered reading companion that helps readers explore books through natural-language questions, semantic search, and AI-generated answers grounded in the original text. It combines PDF reading with Retrieval-Augmented Generation (RAG), allowing users to ask questions about a specific book and receive relevant answers with source-page references.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [How RAG Works](#how-rag-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Supported Books](#supported-books)
- [Evolution from ChromaDB to Qdrant](#evolution-from-chromadb-to-qdrant)
- [Embedding Model and Hosted Inference](#embedding-model-and-hosted-inference)
- [Environment Variables](#environment-variables)
- [Installation and Local Setup](#installation-and-local-setup)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [PDF Reading and Citations](#pdf-reading-and-citations)
- [Ingestion and Vector Migration](#ingestion-and-vector-migration)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Future Improvements](#future-improvements)

---

## Overview

BOOKWORRM aims to make reading more interactive by combining a digital library with an AI assistant that understands the selected book.

Instead of answering questions exclusively from general knowledge, the backend retrieves semantically relevant passages from the selected book and provides them to a Large Language Model (LLM) as context. This helps keep answers connected to the original text and enables source-page references.

The project initially used a completely local retrieval setup based on ChromaDB and Sentence Transformers. During deployment preparation, the vector database was migrated to Qdrant Cloud, and query embedding was moved to Qdrant's hosted inference functionality to reduce the backend's dependency footprint.

### Project Objectives

- Provide an interactive PDF reading experience.
- Answer natural-language questions about individual books.
- Retrieve relevant passages using semantic similarity.
- Keep retrieval isolated by book.
- Preserve page metadata for source citations.
- Store vectors in a managed cloud database.
- Reduce deployment size by avoiding unnecessary local ML dependencies.
- Keep the frontend and backend independently deployable.

---

## Features

### Reading Interface

- Library interface for selecting books.
- PDF reading through a dedicated backend endpoint.
- Book-specific metadata and page information.
- Integration between reading and AI-assisted exploration.

### AI Reading Assistant

- Natural-language question answering.
- Retrieval-Augmented Generation (RAG).
- Semantic retrieval of relevant passages.
- Book-specific vector collections.
- Source text and page metadata for citations.
- LLM-based answer generation using the Groq API.

### Backend

- FastAPI REST API.
- Qdrant Cloud vector storage.
- Cosine-similarity search.
- Environment-variable configuration for credentials.
- Health-check endpoint.
- Interactive Swagger API documentation.

---

## System Architecture

The application consists of a frontend, a Python backend, a hosted vector database, and an LLM service.

```text
                   USER
                    |
                    v
          BOOKWORRM FRONTEND
                  Vercel
                    |
              HTTPS Requests
                    |
                    v
             FASTAPI BACKEND
                    |
          +---------+---------+
          |                   |
          v                   v
     QDRANT CLOUD           GROQ API
   Vector Retrieval       LLM Generation
          |
          v
  Relevant Book Passages
  + Page Metadata
          |
          v
  Context-Aware Answer
  + Source References
```

### Component Responsibilities

**Frontend:** Displays the book library, PDF reader, question interface, answers, and citations.

**FastAPI backend:** Handles API requests, book selection, PDF delivery, retrieval, and answer generation.

**Qdrant Cloud:** Stores vector representations of book chunks and their associated metadata.

**Qdrant hosted inference:** Generates query embeddings remotely using the configured compatible embedding model.

**Groq API:** Generates natural-language answers from the retrieved passages.

**PDF corpus:** Contains the original book PDFs used for reading and ingestion.

---

## How RAG Works

BOOKWORRM uses Retrieval-Augmented Generation rather than relying only on an LLM's pretrained knowledge.

The question-answering process follows these steps:

1. **Question input:** The reader selects a book and asks a question.
2. **Request handling:** The frontend sends the selected `book_id` and question to the FastAPI backend.
3. **Book selection:** The backend selects the vector collection associated with the requested book.
4. **Query embedding:** The question is converted into a vector using the configured embedding model through Qdrant hosted inference.
5. **Semantic retrieval:** Qdrant searches the selected collection for the most relevant chunks.
6. **Context preparation:** The backend receives the retrieved text and metadata, including page numbers.
7. **Answer generation:** The retrieved context is sent to the configured language model through Groq.
8. **Response delivery:** The API returns the generated answer and source information for the frontend to display.

### Why Use Book-Specific Collections?

Each book has its own vector collection. This prevents a question about one book from retrieving passages from another book when the correct book ID is supplied.

For example:

- `jungle_book` maps to `book_jungle_book`.
- `alice_in_wonderland` maps to `book_alice_in_wonderland`.
- `around_the_world` maps to `book_around_the_world`.
- `wuthering_heights` maps to `book_wuthering_heights`.

### Retrieval Metadata

Each indexed chunk preserves relevant metadata:

- `text`: The original text of the chunk.
- `page`: The PDF page associated with the chunk.
- `book_id`: The identifier of the source book.
- `chunk_id`: The original chunk identifier.

This metadata supports book-specific retrieval and page-level source references.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Next.js / React | Frontend interface |
| Python | Backend development |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Qdrant Cloud | Hosted vector database |
| ChromaDB | Original local vector database and migration source |
| Sentence Transformers | Original local embedding implementation |
| `all-MiniLM-L6-v2` | Original 384-dimensional embedding model |
| Qdrant hosted inference | Remote query embedding |
| Groq API | LLM-based answer generation |
| OpenAI Python SDK | OpenAI-compatible client used for model requests |
| PyMuPDF | PDF processing |
| python-dotenv | Local environment-variable loading |
| Vercel | Frontend hosting and attempted backend deployment |

Some technologies are used only in the original local indexing or migration workflow. The production dependency list should contain only packages required by the deployed runtime.

---

## Project Structure

The main project structure is organized as follows:

```text
Jungle-Book-RAG/
│
├── app.py
├── ingest.py
├── list_models.py
├── migrate_to_qdrant.py
├── test_qdrant.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── Data/
│   └── books/
│       ├── jungle_book.pdf
│       ├── alice_in_wonderland.pdf
│       ├── around_the_world_in_80_days.pdf
│       └── wuthering_heights.pdf
│
├── chroma_db/
│   └── Original local vector database
│
└── src/
    ├── book_registry.py
    ├── config.py
    │
    ├── embeddings/
    │   └── embedder.py
    │
    ├── generation/
    │   ├── llm_service.py
    │   └── rag_pipeline.py
    │
    ├── ingestion/
    │   ├── pdf_loader.py
    │   └── chunker.py
    │
    └── retrieval/
        ├── retriever.py
        └── vector_store.py
```

### Important Files

| File | Responsibility |
|---|---|
| `app.py` | FastAPI application, endpoints, and request handling |
| `src/book_registry.py` | Book identifiers, metadata, and PDF lookup |
| `src/config.py` | Application configuration |
| `src/embeddings/embedder.py` | Original local Sentence Transformers wrapper |
| `src/ingestion/pdf_loader.py` | Extracts text from PDFs |
| `src/ingestion/chunker.py` | Splits extracted text into chunks |
| `src/retrieval/retriever.py` | Retrieves relevant chunks for a question |
| `src/retrieval/vector_store.py` | Qdrant client, collection handling, and search |
| `src/generation/llm_service.py` | Calls the configured Groq-compatible LLM API |
| `src/generation/rag_pipeline.py` | Coordinates retrieval and generation |
| `ingest.py` | Original ingestion and indexing workflow |
| `migrate_to_qdrant.py` | Migrates existing ChromaDB vectors into Qdrant |
| `test_qdrant.py` | Retrieval smoke test |

The actual repository may contain additional development scripts and tests.

---

## Supported Books

BOOKWORRM currently supports four books.

| Book ID | Book | Qdrant Collection | Migrated Chunks |
|---|---|---|---:|
| `jungle_book` | The Jungle Book | `book_jungle_book` | 396 |
| `alice_in_wonderland` | Alice's Adventures in Wonderland | `book_alice_in_wonderland` | 238 |
| `around_the_world` | Around the World in Eighty Days | `book_around_the_world` | 499 |
| `wuthering_heights` | Wuthering Heights | `book_wuthering_heights` | 840 |

The migration verification also found a legacy collection named `jungle_book` containing 396 chunks. This collection was retained separately from the current `book_jungle_book` collection.

The counts above reflect the migration verification performed during development. They may change if collections are re-indexed or updated.

---

## Evolution from ChromaDB to Qdrant

### Phase 1: Local ChromaDB Implementation

The original implementation used ChromaDB's persistent client:

```python
chromadb.PersistentClient(path=str(DB_PATH))
```

The database was stored in the project's local `chroma_db/` directory.

Each book had a separate collection, and each collection stored:

- Embedded text chunks.
- Chunk identifiers.
- Page numbers.
- Book IDs.
- Cosine-distance indexing configuration.

The local Sentence Transformers model generated normalized 384-dimensional embeddings using:

`sentence-transformers/all-MiniLM-L6-v2`

During retrieval, the application embedded the user's question locally and queried the corresponding ChromaDB collection.

### Why ChromaDB Was Replaced for Deployment

The local approach was suitable for development but created deployment challenges:

- The local database was stored on the application filesystem.
- Persistent local storage is not guaranteed across serverless instances.
- The original deployment bundle exceeded Vercel's function-size limits.
- Local embedding dependencies introduced a substantial package footprint.

The database itself was approximately 28 MB, while the four PDFs totalled approximately 9 MB. Removing those files alone was not enough to address the multi-gigabyte deployment bundle.

### Phase 2: Migration to Qdrant Cloud

Qdrant Cloud was introduced to store vectors outside the backend deployment.

The migration process:

1. Connected to the existing local ChromaDB database.
2. Enumerated all available collections.
3. Retrieved stored chunk IDs, documents, metadata, and embeddings in batches.
4. Created matching Qdrant collections with 384-dimensional cosine vectors.
5. Converted original chunk identifiers into valid Qdrant point IDs.
6. Uploaded vectors and payload metadata.
7. Verified collection names and point counts.

The migration preserved existing embeddings, so the document vectors did not need to be regenerated.

### Phase 3: Qdrant Hosted Inference

The original local embedder loaded PyTorch and Sentence Transformers to embed every query. This increased the deployment dependency footprint.

The updated retrieval path uses Qdrant's hosted inference interface to embed query text remotely with the compatible MiniLM model.

This allows the deployed API to avoid loading the local embedding model for query retrieval, provided no other runtime module imports or initializes the local model.

### Migration Safety

- Keep the local `chroma_db/` directory as a backup until production testing is complete.
- Do not delete the legacy Qdrant collection without verifying that no code uses it.
- Verify collection counts after migration.
- The migration script may skip collections that already exist. A partially migrated collection must be checked before attempting a retry.
- Do not re-index using a different embedding model without creating compatible vectors for the entire collection.

---

## Embedding Model and Hosted Inference

### Original Embedding Model

The original model was:

`sentence-transformers/all-MiniLM-L6-v2`

It generates 384-dimensional vectors and was used to embed both document chunks and user queries.

### Current Query Embedding

The current retrieval implementation uses Qdrant hosted inference with the same model family. The Qdrant dashboard listed **All MiniLM L6 v2** as a free dense text-embedding model with 384 dimensions.

The Qdrant client must be configured for cloud inference where required by the installed client version.

### Why Model Consistency Matters

The stored document vectors and query vectors must be compatible. Matching vector dimensions alone is not enough: vectors generated by unrelated embedding models may occupy different semantic spaces.

If a new embedding model is introduced, re-embed the document chunks into a separate collection and validate retrieval before switching the application to it.

---

## Environment Variables

Create a local `.env` file in the project root for development.

```env
# Groq API
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=openai/gpt-oss-safeguard-20b

# Qdrant Cloud
QDRANT_URL=https://your-qdrant-cluster-endpoint
QDRANT_API_KEY=your-qdrant-api-key
```

Use the exact values supplied by your providers.

### Variable Descriptions

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Secret key used for language-model requests |
| `GROQ_MODEL` | Model identifier configured for answer generation |
| `QDRANT_URL` | HTTPS endpoint of the Qdrant Cloud cluster |
| `QDRANT_API_KEY` | Credential used to access the Qdrant cluster |
| `NEXT_PUBLIC_API_URL` | Frontend environment variable containing the public backend URL |

`NEXT_PUBLIC_API_URL` belongs in the frontend project's environment settings, not in a public backend secret configuration.

**Never commit `.env` or expose provider keys in frontend JavaScript.**

An `.env.example` file should contain placeholder values only.

---

## Installation and Local Setup

### Prerequisites

- Python installed and available on the command line.
- Git.
- A Qdrant Cloud cluster and API key.
- A Groq API key.
- The project repository and required book PDFs.

### 1. Clone the Repository

```bash
git clone https://github.com/Vandan1309/BOOKWORRM.git
cd BOOKWORRM
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure `.env`

Create the `.env` file in the repository root and add the required Qdrant and Groq variables.

Each line should use the format:

```text
KEY=value
```

If `python-dotenv` prints parsing warnings, correct the malformed lines before continuing.

---

## Running the Application

### Start the Backend

```powershell
uvicorn app:app --reload
```

The development API should be available at:

- **API root:** `http://127.0.0.1:8000/`
- **Health check:** `http://127.0.0.1:8000/health`
- **Swagger documentation:** `http://127.0.0.1:8000/docs`

Keep the terminal open while testing. Stop the server using `Ctrl+C`.

### Test Qdrant Retrieval

The project includes a retrieval smoke test that uses the `jungle_book` collection.

Example:

```python
from src.retrieval.retriever import Retriever

retriever = Retriever(book_id="jungle_book")
results = retriever.retrieve("Who is Mowgli?", top_k=3)

for result in results:
    print(result["book_id"], result["page"], result["distance"])
    print(result["text"][:300])
```

A successful test should return relevant passages and their page metadata.

### Test the Full RAG Pipeline

1. Start the API.
2. Open `http://127.0.0.1:8000/docs`.
3. Expand `POST /ask`.
4. Select **Try it out**.
5. Submit the following request:

```json
{
  "book_id": "jungle_book",
  "question": "Who is Mowgli?"
}
```

6. Click **Execute**.
7. Check that the response contains an answer and source-page information.

Repeat the test with another book to confirm that retrieval uses the correct collection.

---

## API Reference

The backend currently exposes these endpoints.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Basic API response |
| `GET` | `/health` | Health check |
| `GET` | `/books` | Lists available books |
| `GET` | `/books/{book_id}/details` | Returns selected-book metadata |
| `GET` | `/books/{book_id}/pdf` | Serves the selected PDF |
| `POST` | `/ask` | Answers a question about a selected book |

Use `/docs` as the source of truth for the exact request and response schemas.

### Example: `POST /ask`

Request:

```json
{
  "book_id": "jungle_book",
  "question": "Who is Mowgli?"
}
```

The backend selects the corresponding vector collection, retrieves relevant passages, and sends the context to the configured LLM. The response structure is defined by the current implementation in `app.py`.

---

## PDF Reading and Citations

The PDF reading flow is separate from vector retrieval.

1. The frontend requests book metadata.
2. The frontend loads the PDF using `/books/{book_id}/pdf`.
3. The question-answering pipeline retrieves relevant chunks with page metadata.
4. The LLM generates a response using the retrieved text.
5. The frontend displays the answer and source references.

Citation accuracy depends on preserving page metadata throughout PDF extraction, chunking, vector migration, and answer generation.

If PDF files are excluded from the backend deployment, the PDF endpoint must be updated to serve them from an external location such as object storage.

---

## Ingestion and Vector Migration

### Original Ingestion Workflow

The original ingestion pipeline:

1. Reads the PDF files from `Data/books/`.
2. Extracts text and page information.
3. Splits the extracted text into chunks.
4. Generates embeddings with Sentence Transformers.
5. Stores the vectors, text, and metadata in ChromaDB.

### Migration Workflow

The one-time migration script transfers existing embeddings from ChromaDB into Qdrant Cloud. It does not need to regenerate document embeddings because the original vectors are read from ChromaDB and uploaded directly.

### Adding a New Book

Adding a book requires:

1. Adding the PDF file.
2. Registering the book ID, title, and filename.
3. Extracting and chunking the PDF text.
4. Generating embeddings using the compatible embedding model.
5. Creating and populating the corresponding Qdrant collection.
6. Updating the frontend library if the new book should be selectable.
7. Testing PDF delivery, retrieval, answers, and citations.

**Important:** the original ingestion script may still import ChromaDB or Sentence Transformers. Removing these packages from the production dependency list does not automatically update the ingestion workflow. Keep ingestion as a separate development or worker process unless it has been adapted to the new architecture.

---

## Deployment

### Frontend Deployment

The frontend is maintained as a separate Vercel project.

Set the frontend environment variable:

```env
NEXT_PUBLIC_API_URL=https://your-live-backend-domain
```

Replace the placeholder with the actual public HTTPS URL of the deployed backend, then redeploy the frontend.

Do not use `127.0.0.1` or `localhost` in production frontend configuration.

### Backend Deployment

The backend requires a Python runtime, outbound HTTPS connectivity, and access to Qdrant Cloud and Groq.

Configure these environment variables in the backend hosting dashboard:

- `QDRANT_URL`
- `QDRANT_API_KEY`
- `GROQ_API_KEY`
- `GROQ_MODEL`

Also verify that:

- `requirements.txt` includes all dependencies used during API startup and requests.
- Removed dependencies are not imported by deployed runtime modules.
- PDFs are included in the deployment or hosted externally.
- The health-check path matches the API (`/health`).
- CORS permits the deployed frontend origin.
- Qdrant hosted inference works in the deployed environment.

### Vercel Bundle-Size Optimization

The original deployment bundle was approximately 5.9–6.0 GB. Even after enabling an extended function-size limit of 5,120 MB, it remained too large.

The main optimization strategy is to:

- Move vector storage to Qdrant Cloud.
- Exclude the local `chroma_db/` directory from the deployed runtime.
- Avoid packaging the local embedding model and PyTorch stack when query embedding is performed by Qdrant hosted inference.
- Remove unused dependencies only after checking imports.
- Keep development scripts and migration utilities out of the runtime import path.

Removing `chromadb` or `sentence-transformers` from `requirements.txt` is safe only if the deployed application does not import them during startup or request handling.

A deployment is not considered complete until the live `/health`, `/books`, PDF, and `/ask` endpoints have been tested.

### Current Status

The local Qdrant migration, retrieval test, and full local `/ask` test were successful during development. The final deployment with the reduced dependency list must still be verified.

---

## Troubleshooting

### Qdrant Environment Variable Missing

Check that `.env` is in the project root and `load_dotenv()` runs before environment variables are accessed. For production, set the variables in the hosting dashboard.

### Qdrant Connection Error

- Verify that the cluster is healthy.
- Copy the exact HTTPS endpoint from Qdrant Cloud.
- Check outbound network access.
- Verify the API key.

### Hosted Inference Model Error

- Confirm that the model appears in the Qdrant Cloud inference catalogue.
- Ensure the client is configured for cloud inference where required.
- Verify model compatibility with the existing stored vectors.
- Avoid changing embedding models without re-indexing the documents.

### Empty or Irrelevant Retrieval Results

- Verify that the selected collection exists and contains vectors.
- Check the book ID-to-collection mapping.
- Confirm that query and document embeddings are compatible.
- Inspect the stored payload for `text`, `page`, and `book_id`.

### `.env` Parsing Warnings

Each environment variable should be written on its own line in `KEY=value` format. Remove malformed lines, pasted terminal output, and accidental extra text.

### PDF Endpoint Errors

Check that the book ID exists in the registry, the PDF filename matches the actual file, and the file is available in the deployed environment.

### Deployment Bundle Still Too Large

Inspect the build logs and final bundle-size message. Check for dependencies pulled in transitively and imports of local ML packages. Exclude local databases, caches, tests, and virtual environments when they are not required at runtime.

---

## Security

- Never commit `.env`.
- Never expose Groq or Qdrant credentials in frontend code.
- Use HTTPS for deployed services.
- Restrict CORS to the production frontend domain where practical.
- Avoid logging API keys or sensitive request headers.
- Keep a backup of the original ChromaDB database until production migration has been verified.
- Treat free-tier limits and provider policies as subject to change.

---

## Future Improvements

Potential next steps include:

- Automated evaluation of retrieval relevance and citation accuracy.
- Improved error handling for LLM and vector database failures.
- Structured logging and request-latency monitoring.
- External PDF storage for more scalable reading.
- A dedicated ingestion workflow independent of the API runtime.
- Automated deployment checks for the health endpoint and question-answering flow.
- More books and improved library metadata.
- Monitoring provider usage and free-tier limits.

---

## Maintainer

**BOOKWORRM** — Your AI-Assisted Bookmark

*Stay curious. Go beyond the page.*
