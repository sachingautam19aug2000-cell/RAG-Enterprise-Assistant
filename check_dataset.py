import os

project_path = os.path.dirname(os.path.abspath(__file__))

print("Project location:")
print(project_path)

print("\nProject folders/files:")
for item in os.listdir(project_path):
    print(item)
import os

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

print("DATASET LOCATION:")
print(data_path)

print("\nALL DATASET FILES:")

for root, folders, files in os.walk(data_path):
    for file in files:
        full_path = os.path.join(root, file)
        relative_path = os.path.relpath(full_path, data_path)
        print(relative_path)


        import os

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

print("=" * 60)
print("RAG DATASET SUMMARY")
print("=" * 60)

total_files = 0
total_folders = 0

for root, folders, files in os.walk(data_path):
    total_folders += len(folders)
    total_files += len(files)

print("\nDataset path:")
print(data_path)

print("\nTotal folders:", total_folders)
print("Total files:", total_files)

print("\nFile types:")

file_types = {}

for root, folders, files in os.walk(data_path):
    for file in files:
        extension = os.path.splitext(file)[1].lower()

        if extension == "":
            extension = "[no extension]"

        file_types[extension] = file_types.get(extension, 0) + 1

for extension, count in sorted(file_types.items()):
    print(extension, ":", count)

print("\nTop-level contents:")

for item in os.listdir(data_path):
    full_path = os.path.join(data_path, item)

    if os.path.isdir(full_path):
        print("[FOLDER]", item)
    else:
        print("[FILE]  ", item)

print("\n" + "=" * 60)
print("SUMMARY COMPLETE")
print("=" * 60)
import os

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

print("=" * 60)
print("SEARCHING DATASET DOCUMENTS")
print("=" * 60)

supported_files = []

for root, folders, files in os.walk(data_path):
    for file in files:
        extension = os.path.splitext(file)[1].lower()

        if extension in [".txt", ".md", ".pdf", ".json"]:
            full_path = os.path.join(root, file)
            supported_files.append(full_path)

print("\nTotal supported files found:", len(supported_files))

print("\nFirst 10 files:")

for file in supported_files[:10]:
    print(os.path.relpath(file, data_path))

print("\n" + "=" * 60)



import os

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

supported_files = []

for root, folders, files in os.walk(data_path):
    for file in files:
        extension = os.path.splitext(file)[1].lower()

        if extension in [".txt", ".md"]:
            full_path = os.path.join(root, file)
            supported_files.append(full_path)

print("=" * 60)
print("DOCUMENT READING TEST")
print("=" * 60)

if len(supported_files) == 0:
    print("\nNo TXT/MD document found.")
else:
    first_file = supported_files[0]

    print("\nReading:")
    print(os.path.relpath(first_file, data_path))

    print("\n" + "-" * 60)

    with open(first_file, "r", encoding="utf-8") as file:
        text = file.read()

    print(text[:5000])

    print("\n" + "-" * 60)
    print("Characters read:", len(text))
    print("=" * 60)
