import os
import json

project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, "Data")

json_files = []

for root, folders, files in os.walk(data_path):
    for file in files:
        if file.lower().endswith(".json"):
            json_files.append(os.path.join(root, file))

print("=" * 60)
print("JSON DATASET INSPECTION")
print("=" * 60)

print("Total JSON files:", len(json_files))

if len(json_files) > 0:

    first_file = json_files[0]

    print("\nFirst JSON file:")
    print(os.path.relpath(first_file, data_path))

    print("\n" + "-" * 60)

    try:
        with open(first_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("JSON type:", type(data).__name__)

        if isinstance(data, dict):
            print("Keys:")
            for key in list(data.keys())[:20]:
                print("-", key)

        elif isinstance(data, list):
            print("Number of records:", len(data))

            if len(data) > 0:
                print("\nFirst record:")
                print(data[0])

    except Exception as e:
        print("Error reading JSON:", e)

print("=" * 60)
