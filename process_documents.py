import os
import re
import json

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# 1. PROJECT PATHS
# ============================================================

project_path = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(project_path, "Data")

processed_path = os.path.join(
    project_path,
    "processed_chunks.json"
)

vector_db_path = os.path.join(
    project_path,
    "vector_database"
)


# ============================================================
# 2. SETTINGS
# ============================================================

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


# ============================================================
# 3. CLEAN TEXT
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
# 4. CREATE CHUNKS
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
# 5. READ ALL MARKDOWN DOCUMENTS
# ============================================================

print("=" * 60)
print("STEP 1 - READING DOCUMENTS")
print("=" * 60)

md_files = []

for root, folders, files in os.walk(data_path):

    for file in files:

        if file.lower().endswith(".md"):

            full_path = os.path.join(
                root,
                file
            )

            md_files.append(full_path)


print("Markdown documents found:", len(md_files))


# ============================================================
# 6. CLEAN + CHUNK ALL DOCUMENTS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2 - CLEANING AND CHUNKING")
print("=" * 60)

all_chunks = []

for document_number, file_path in enumerate(
    md_files,
    start=1
):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()


    cleaned_text = clean_text(text)

    chunks = create_chunks(
        cleaned_text
    )


    source_name = os.path.relpath(
        file_path,
        data_path
    )


    for chunk_number, chunk in enumerate(
        chunks,
        start=1
    ):

        all_chunks.append({

            "chunk_id":
                f"{document_number}_{chunk_number}",

            "source":
                source_name,

            "chunk_number":
                chunk_number,

            "text":
                chunk
        })


    print(
        f"Processed {document_number}/{len(md_files)}"
    )


# ============================================================
# 7. SAVE PROCESSED CHUNKS
# ============================================================

with open(
    processed_path,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        ensure_ascii=False
    )


print("\nTotal chunks created:", len(all_chunks))


# ============================================================
# 8. LOAD EMBEDDING MODEL
# ============================================================

print("\n" + "=" * 60)
print("STEP 3 - LOADING EMBEDDING MODEL")
print("=" * 60)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# ============================================================
# 9. CREATE VECTOR DATABASE
# ============================================================

print("\n" + "=" * 60)
print("STEP 4 - CREATING VECTOR DATABASE")
print("=" * 60)

client = chromadb.PersistentClient(
    path=vector_db_path
)

collection = client.get_or_create_collection(
    name="enterprise_documents"
)


# ============================================================
# 10. ADD EMBEDDINGS
# ============================================================

print("\nCreating embeddings...")

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

    metadatas = [

        {
            "source":
                item["source"],

            "chunk_number":
                item["chunk_number"]
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

        metadatas=metadatas
    )


    print(
        f"Stored {min(start + batch_size, len(all_chunks))}"
        f"/{len(all_chunks)} chunks"
    )


print("\nVector database ready.")

print(
    "Total vectors:",
    collection.count()
)


# ============================================================
# 11. RAG RETRIEVAL TEST
# ============================================================

print("\n" + "=" * 60)
print("STEP 5 - RAG RETRIEVAL TEST")
print("=" * 60)


question = input(
    "\nEnter your question: "
)


# Convert question into embedding

question_embedding = embedding_model.encode(
    [question]
).tolist()


# Search relevant chunks

results = collection.query(

    query_embeddings=question_embedding,

    n_results=5
)


# ============================================================
# 12. DISPLAY RESULTS
# ============================================================

print("\n" + "-" * 60)
print("TOP RELEVANT DOCUMENTS")
print("-" * 60)


documents = results["documents"][0]

metadatas = results["metadatas"][0]


for i, (
    document,
    metadata
) in enumerate(
    zip(documents, metadatas),
    start=1
):

    print(f"\nRESULT {i}")

    print(
        "Source:",
        metadata["source"]
    )

    print(
        "Chunk:",
        metadata["chunk_number"]
    )

    print("\nText:")

    print(
        document[:1000]
    )

    print(
        "-" * 60
    )


print("\nRAG retrieval completed.")

print("=" * 60)
