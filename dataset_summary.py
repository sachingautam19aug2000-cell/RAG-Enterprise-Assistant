import os

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

md_files = []

for root, folders, files in os.walk(data_path):
    for file in files:
        if file.lower().endswith(".md"):
            md_files.append(os.path.join(root, file))

print("=" * 60)
print("MARKDOWN DATASET SUMMARY")
print("=" * 60)

total_characters = 0

for file_path in md_files:

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    total_characters += len(text)

print("Total Markdown documents:", len(md_files))
print("Total characters:", total_characters)

if len(md_files) > 0:
    average = total_characters / len(md_files)
    print("Average characters per document:", round(average))

print("=" * 60)
