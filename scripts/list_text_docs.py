import json
from pathlib import Path

DATA_DIR = Path(r"c:\Users\tlima\Downloads\SIMP-PE\data")
with open(DATA_DIR / "catalog_raw.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

text_docs = [item for item in catalog if item["ext"] in [".pdf", ".docx", ".txt", ".pptx", ".odt", ".md"]]

print(f"Total de documentos de texto/manuais: {len(text_docs)}")

docs_by_folder = {}
for doc in text_docs:
    folder = doc["top_folder"]
    docs_by_folder.setdefault(folder, []).append(doc)

for folder, docs in sorted(docs_by_folder.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n=== Pasta: {folder} ({len(docs)} docs) ===")
    for d in docs[:10]: # Primeiros 10
        print(f"  - [{d['ext']}] {d['relative_path']} ({d['size_mb']} MB)")
    if len(docs) > 10:
        print(f"  ... e mais {len(docs) - 10} documentos.")
