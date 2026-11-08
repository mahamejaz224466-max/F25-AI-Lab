import json
from pathlib import Path

with open("corpus.json", encoding="utf-8") as file:
    docs = json.load(file)

with open("queries.json", encoding="utf-8") as file:
    queries = json.load(file)

print("Dataset already exists.")
print("Documents:", len(docs))
print("Queries:", len(queries))
