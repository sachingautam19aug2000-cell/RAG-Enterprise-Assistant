import os

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

print("=" * 60)
print("DATASET FILE TYPES")
print("=" * 60)

file_count = 0
extensions = {}

for root, folders, files in os.walk(data_path):
    for file in files:
        file_count += 1

        ext = os.path.splitext(file)[1].lower()

        if ext == "":
            ext = "[no extension]"

        extensions[ext] = extensions.get(ext, 0) + 1

print("\nTotal files:", file_count)

print("\nFile types:")
for ext, count in sorted(extensions.items()):
    print(ext, "->", count)

print("\nSample files:")

shown = 0

for root, folders, files in os.walk(data_path):
    for file in files:
        print(os.path.relpath(os.path.join(root, file), data_path))
        shown += 1

        if shown >= 15:
            break

    if shown >= 15:
        break

print("=" * 60)
