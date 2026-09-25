
import os
import re
import json
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200



import os
import re
import json

import chromadb
from sentence_transformers import SentenceTransformer
from google import genai


# ============================================================
# PROJECT SETTINGS
# ============================================================

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    PROJECT_PATH,
    "Data"
)

PROCESSED_FILE = os.path.join(
    PROJECT_PATH,
    "processed_chunks.json"
)

VECTOR_DB_PATH = os.path.join(
    PROJECT_PATH,
    "vector_database"
)

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    text = text.replace("\x00", " ")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(text):

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - CHUNK_OVERLAP

    return chunks


# ============================================================
# STEP 1 - FIND DOCUMENTS
# ============================================================

print("=" * 60)
print("RAG ENTERPRISE KNOWLEDGE ASSISTANT")
print("=" * 60)

print("\nSTEP 1 - FINDING DOCUMENTS")

md_files = []

for root, folders, files in os.walk(DATA_PATH):

    for file in files:

        if file.lower().endswith(".md"):

            md_files.append(
                os.path.join(root, file)
            )

print(
    "Markdown documents found:",
    len(md_files)
)


# ============================================================
# STEP 2 - CLEAN + CHUNK
# ============================================================

print("\nSTEP 2 - CLEANING AND CHUNKING")

all_chunks = []

for number, file_path in enumerate(
    md_files,
    start=1
):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    cleaned = clean_text(text)

    chunks = create_chunks(cleaned)

    source = os.path.relpath(
        file_path,
        DATA_PATH
    )

    for chunk_number, chunk in enumerate(
        chunks,
        start=1
    ):

        all_chunks.append({

            "chunk_id":
                f"{number}_{chunk_number}",

            "source":
                source,

            "chunk_number":
                chunk_number,

            "text":
                chunk
        })

    print(
        f"Processed {number}/{len(md_files)}"
    )


print(
    "\nTotal chunks:",
    len(all_chunks)
)


# ============================================================
# STEP 3 - SAVE CHUNKS
# ============================================================

with open(
    PROCESSED_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        ensure_ascii=False
    )

print(
    "Chunks saved to:",
    PROCESSED_FILE
)


# ============================================================
# STEP 4 - LOAD EMBEDDING MODEL
# ============================================================

print("\nSTEP 3 - LOADING EMBEDDING MODEL")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# ============================================================
# STEP 5 - CREATE CHROMADB
# ============================================================

print("\nSTEP 4 - CREATING VECTOR DATABASE")

client = chromadb.PersistentClient(
    path=VECTOR_DB_PATH
)

collection = client.get_or_create_collection(
    name="enterprise_documents"
)

print("Vector database ready.")


# ============================================================
# STEP 6 - STORE EMBEDDINGS
# ============================================================

print("\nSTEP 5 - CREATING EMBEDDINGS")

batch_size = 100

for start in range(
    0,
    len(all_chunks),
    batch_size
):

    batch = all_chunks[
        start:start + batch_size
    ]

    texts = [
        item["text"]
        for item in batch
    ]

    ids = [
        item["chunk_id"]
        for item in batch
    ]

    metadata = [

        {
            "source": item["source"],
            "chunk_number": item["chunk_number"]
        }

        for item in batch
    ]

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=False
    ).tolist()

    collection.upsert(

        ids=ids,

        documents=texts,

        embeddings=embeddings,

        metadatas=metadata
    )

    print(
        f"Stored {min(start + batch_size, len(all_chunks))}"
        f"/{len(all_chunks)}"
    )


print(
    "\nTotal vectors:",
    collection.count()
)


# ============================================================
# STEP 7 - GEMINI CONNECTION
# ============================================================

print("\nSTEP 6 - CONNECTING GEMINI")

try:

    gemini_client = genai.Client()

    print("Gemini connection successful.")

except Exception as error:

    print("Gemini connection failed.")
    print(error)

    raise SystemExit


# ============================================================
# STEP 8 - ASK QUESTION
# ============================================================

print("\n" + "=" * 60)
print("RAG QUESTION ANSWERING")
print("=" * 60)

question = input(
    "\nEnter your question: "
)


# ============================================================
# STEP 9 - QUESTION EMBEDDING
# ============================================================

question_embedding = embedding_model.encode(
    [question]
).tolist()


# ============================================================
# STEP 10 - RETRIEVE RELEVANT CHUNKS
# ============================================================

results = collection.query(

    query_embeddings=question_embedding,

    n_results=5
)

documents = results["documents"][0]

metadatas = results["metadatas"][0]


print("\nRelevant sources found:")

for i, metadata in enumerate(
    metadatas,
    start=1
):

    print(
        f"{i}. {metadata['source']}"
    )


# ============================================================
# STEP 11 - BUILD CONTEXT
# ============================================================

context_parts = []

for i, (
    document,
    metadata
) in enumerate(
    zip(documents, metadatas),
    start=1
):

    context_parts.append(

        f"[SOURCE {i}]\n"
        f"Document: {metadata['source']}\n"
        f"Chunk: {metadata['chunk_number']}\n"
        f"Content:\n{document}"
    )


context = "\n\n".join(
    context_parts
)


# ============================================================
# STEP 12 - GEMINI ANSWER
# ============================================================

prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question ONLY using the
provided context.

If the answer cannot be found in the context,
say: "I could not find this information in the
provided documents."

Do not invent facts.

Always mention the source document used.

USER QUESTION:
{question}

CONTEXT:
{context}
"""


print("\nGenerating answer...")


interaction = gemini_client.interactions.create(

    model="gemini-3.8-flash",

    input=prompt
)


answer = interaction.output_text


# ============================================================
# STEP 13 - DISPLAY FINAL ANSWER
# ============================================================

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(answer)

print("\n" + "=" * 60)
print("SOURCES")
print("=" * 60)

for i, metadata in enumerate(
    metadatas,
    start=1
):

    print(
        f"{i}. {metadata['source']}"
    )

print("\nRAG PIPELINE COMPLETED.")

print("=" * 60)


# ============================================================
# STEP 13 - SAVE QUERY LOG
# ============================================================

from datetime import datetime

LOG_FILE = os.path.join(
    PROJECT_PATH,
    "query_logs.json"
)

query_log = {
    "timestamp": datetime.now().isoformat(),
    "question": question,
    "answer": answer,
    "sources": [
        metadata["source"]
        for metadata in metadatas
    ]
}

existing_logs = []

if os.path.exists(LOG_FILE):

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        try:
            existing_logs = json.load(f)

        except json.JSONDecodeError:
            existing_logs = []

existing_logs.append(query_log)

with open(
    LOG_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        existing_logs,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nQuery log saved successfully.")


answer = interaction.output_text


# SAVE QUERY TO SQLITE DATABASE

import sqlite3

db_path = os.path.join(
    PROJECT_PATH,
    "rag_assistant.db"
)

connection = sqlite3.connect(db_path)

cursor = connection.cursor()

cursor.execute(
    """
    INSERT INTO rag_query_logs
    (timestamp, question, answer, sources)
    VALUES (datetime('now'), ?, ?, ?)
    """,
    (
        question,
        answer,
        ", ".join(
            metadata["source"]
            for metadata in metadatas
        )
    )
)

connection.commit()
connection.close()

print("Query saved to SQLite database.")
