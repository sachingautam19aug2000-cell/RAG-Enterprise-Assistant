import os
import re

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def clean_text(text):
    text = text.replace("\x00", " ")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def create_chunks(text, chunk_size=1200, overlap=200):

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


print("=" * 60)
print("DOCUMENT CLEANING AND CHUNKING TEST")
print("=" * 60)

md_files = []

for root, folders, files in os.walk(data_path):
    for file in files:

        if file.lower().endswith(".md"):
            md_files.append(os.path.join(root, file))

print("Documents found:", len(md_files))

if len(md_files) > 0:

    first_file = md_files[0]

    with open(first_file, "r", encoding="utf-8") as f:
        text = f.read()

    print("\nOriginal characters:", len(text))

    cleaned_text = clean_text(text)

    print("Cleaned characters:", len(cleaned_text))

    chunks = create_chunks(
        cleaned_text,
        CHUNK_SIZE,
        CHUNK_OVERLAP
    )

    print("Chunks created:", len(chunks))

    print("\n" + "-" * 60)
    print("FIRST CHUNK")
    print("-" * 60)

    print(chunks[0])

    print("\n" + "-" * 60)
    print("SECOND CHUNK")
    print("-" * 60)

    if len(chunks) > 1:
        print(chunks[1])

print("=" * 60)
