import os
import sys
import json
from pathlib import Path

ROOT_DIR = Path(r"G:\Drives compartilhados\DEMSI\04 - PROJETOS\Sistema Unico SIMP4")
OUTPUT_DIR = Path(r"c:\Users\tlima\Downloads\SIMP-PE\data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def scan_files():
    print(f"Escaneando pasta: {ROOT_DIR}")
    catalog = []
    summary_by_ext = {}
    summary_by_folder = {}

    for root, dirs, files in os.walk(ROOT_DIR):
        rel_folder = os.path.relpath(root, ROOT_DIR)
        top_folder = rel_folder.split(os.sep)[0] if rel_folder != "." else "RAIZ"
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            try:
                stat = os.stat(file_path)
                size_bytes = stat.st_size
                mtime = stat.st_mtime
            except Exception as e:
                size_bytes = 0
                mtime = 0

            item = {
                "name": file,
                "ext": ext,
                "relative_path": os.path.relpath(file_path, ROOT_DIR),
                "full_path": file_path,
                "top_folder": top_folder,
                "size_bytes": size_bytes,
                "size_mb": round(size_bytes / (1024 * 1024), 2),
                "mtime": mtime
            }
            catalog.append(item)

            summary_by_ext[ext] = summary_by_ext.get(ext, 0) + 1
            summary_by_folder[top_folder] = summary_by_folder.get(top_folder, 0) + 1

    catalog_path = OUTPUT_DIR / "catalog_raw.json"
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    summary = {
        "total_files": len(catalog),
        "total_size_mb": round(sum(item["size_bytes"] for item in catalog) / (1024 * 1024), 2),
        "by_extension": summary_by_ext,
        "by_top_folder": summary_by_folder
    }

    summary_path = OUTPUT_DIR / "catalog_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Total de arquivos encontrados: {len(catalog)}")
    print(f"Tamanho total: {summary['total_size_mb']} MB")
    print("\nArquivos por extensão:")
    for ext, count in sorted(summary_by_ext.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext if ext else '(sem ext)'}: {count}")

    print("\nArquivos por pasta principal:")
    for folder, count in sorted(summary_by_folder.items(), key=lambda x: x[1], reverse=True):
        print(f"  {folder}: {count}")

if __name__ == "__main__":
    scan_files()
