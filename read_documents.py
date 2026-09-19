import os

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

md_files = []

for root, folders, files in os.walk(data_path):
    for file in files:
        if file.lower().endswith(".md"):
            md_files.append(os.path.join(root, file))

print("=" * 60)
print("MARKDOWN DOCUMENT TEST")
print("=" * 60)

print("Total Markdown documents:", len(md_files))

if len(md_files) > 0:

    first_file = md_files[0]

    print("\nFirst document:")
    print(os.path.relpath(first_file, data_path))

    print("\n" + "-" * 60)

    with open(first_file, "r", encoding="utf-8") as f:
        text = f.read()

    print(text[:5000])

    print("\n" + "-" * 60)
    print("Characters in document:", len(text))

else:
    print("No Markdown documents found.")

print("=" * 60)
