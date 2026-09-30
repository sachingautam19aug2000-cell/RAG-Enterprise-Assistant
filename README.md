# RAG Enterprise Knowledge Assistant

A Retrieval-Augmented Generation (RAG) based enterprise knowledge assistant that retrieves relevant information from enterprise documents and generates grounded answers with source references.

## Overview

This project demonstrates an end-to-end RAG pipeline for enterprise knowledge retrieval.

The system processes enterprise documents, creates semantic embeddings, stores them in a vector database, retrieves relevant context for a user query, and uses an LLM to generate a grounded response.

## Architecture

User Query
    ↓
Query Embedding
    ↓
Semantic Retrieval
    ↓
ChromaDB Vector Database
    ↓
Relevant Document Chunks
    ↓
Context Construction
    ↓
Gemini LLM
    ↓
Grounded Answer + Sources
    ↓
PostgreSQL Logging
    ↓
Power BI Analytics

## Key Features

- Enterprise document ingestion
- Text cleaning and chunking
- Semantic embeddings
- Vector similarity search
- ChromaDB vector database
- Gemini-powered answer generation
- Source-aware responses
- PostgreSQL logging
- Power BI analytics dashboard
- Retrieval evaluation

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | RAG pipeline |
| Sentence Transformers | Text embeddings |
| ChromaDB | Vector database |
| Gemini | Answer generation |
| PostgreSQL | Query/log storage |
| Power BI | Analytics dashboard |
| Git/GitHub | Version control |

## Dataset

The project uses an enterprise document/question dataset containing Markdown documents and evaluation questions.

The raw dataset is not included in the repository when it is too large; the project documentation describes the source and expected directory structure.

## RAG Pipeline

### 1. Document Processing

Enterprise Markdown documents are loaded and cleaned before further processing.

### 2. Chunking

Documents are divided into overlapping chunks to improve retrieval quality.

### 3. Embeddings

Each chunk is converted into a semantic vector using a Sentence Transformer model.

### 4. Vector Storage

Embeddings and document metadata are stored in ChromaDB.

### 5. Retrieval

For every user question, the question is embedded and the most relevant document chunks are retrieved using vector similarity.

### 6. Generation

The retrieved context is passed to Gemini with instructions to answer only from the provided context.

### 7. Source Attribution

The system returns the source documents used to construct the answer.

## Evaluation

The project evaluates retrieval and answer generation using the provided evaluation questions.

Evaluation results are stored in:

`evaluation/evaluation_results.csv`

Metrics should be interpreted according to the evaluation methodology and dataset used.

## Dashboard

The Power BI dashboard provides analytics for:

- Query volume
- Document usage
- Retrieval scores
- Dataset characteristics
- Question analysis
- Recent questions and answers

Dashboard file:

`PowerBI/RAG_Enterprise_Analytics_Final.pbix`

## Project Structure

```text
RAG-Enterprise-Assistant/
│
├── process_documents.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── SQL/
├── PowerBI/
├── evaluation/
├── docs/
└── Data/
