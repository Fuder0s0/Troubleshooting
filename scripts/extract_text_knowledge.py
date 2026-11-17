import os
import sys
import json
import traceback
from pathlib import Path
import pypdf
import docx

ROOT_DIR = Path(r"G:\Drives compartilhados\DEMSI\04 - PROJETOS\Sistema Unico SIMP4")
OUTPUT_DIR = Path(r"c:\Users\tlima\Downloads\SIMP-PE\data\extracted")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Lista de pastas e padrões prioritários para base de conhecimento
PRIORITY_FOLDERS = [
    "6 - Documentação gerada no MPPE",
    "7 - SIMP - Material de Treinamento",
    "2 - Analise do SIMP",
    "5 - Gestao de conhecimento MPMT",
    "8 - PARAMETRIZACAO",
    "9-Resolução SIMP 2026",
    "4 - Projeto Piloto",
    "z_outrosDocumentos"
]

def extract_pdf(pdf_path):
    text_content = []
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        for i, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_content.append(f"--- [Página {i+1}] ---\n{page_text}")
            except Exception as e:
                text_content.append(f"--- [Página {i+1}: erro extração: {e}] ---")
        return num_pages, "\n\n".join(text_content)
    except Exception as e:
        return 0, f"Erro ao abrir PDF: {e}"

def extract_docx(docx_path):
    try:
        doc = docx.Document(str(docx_path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(f"[Tabela] {row_text}")
        return len(paragraphs), "\n\n".join(paragraphs)
    except Exception as e:
        return 0, f"Erro ao ler DOCX: {e}"

def extract_txt_md(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return len(content.splitlines()), content
    except Exception as e:
        return 0, f"Erro ao ler TXT/MD: {e}"

def run_extraction():
    catalog_path = Path(r"c:\Users\tlima\Downloads\SIMP-PE\data\catalog_raw.json")
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Filtrar arquivos textuais
    # Excluir dados de testes com nomes de pessoas ou arquivos pesados de processos individuais se desnecessários
    eligible_docs = []
    for item in catalog:
        if item["top_folder"] in PRIORITY_FOLDERS and item["ext"] in [".pdf", ".docx", ".txt", ".md"]:
            # Ignorar arquivos de dados de processos individuais em "3 - Dados de Processos e Testes" para não poluir
            eligible_docs.append(item)

    print(f"Total de documentos priorizados para extração: {len(eligible_docs)}")

    extracted_index = []
    for idx, doc_info in enumerate(eligible_docs, 1):
        rel_path = doc_info["relative_path"]
        full_path = doc_info["full_path"]
        ext = doc_info["ext"]
        top_folder = doc_info["top_folder"]
        size_mb = doc_info["size_mb"]

        clean_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in Path(rel_path).name)
        safe_rel = "".join(c if c.isalnum() or c in "._- " else "_" for c in rel_path.replace(os.sep, "_"))
        out_txt_name = f"{safe_rel}.txt"
        out_txt_path = OUTPUT_DIR / out_txt_name

        print(f"[{idx}/{len(eligible_docs)}] Extraindo ({ext}, {size_mb} MB): {Path(rel_path).name[:40]}...")

        num_elements = 0
        content = ""
        if ext == ".pdf":
            num_elements, content = extract_pdf(full_path)
        elif ext == ".docx":
            num_elements, content = extract_docx(full_path)
        elif ext in [".txt", ".md"]:
            num_elements, content = extract_txt_md(full_path)

        # Salva o texto extraído
        if content:
            with open(out_txt_path, "w", encoding="utf-8") as f_out:
                f_out.write(f"DOCUMENTO: {rel_path}\nPASTA: {top_folder}\nTAMANHO: {size_mb} MB\n\n{content}")

        extracted_index.append({
            "original_path": rel_path,
            "top_folder": top_folder,
            "filename": Path(rel_path).name,
            "ext": ext,
            "size_mb": size_mb,
            "extracted_file": str(out_txt_path.relative_to(Path(r"c:\Users\tlima\Downloads\SIMP-PE"))),
            "content_char_count": len(content),
            "elements_count": num_elements,
            "has_error": "Erro ao" in content[:100]
        })

    index_path = Path(r"c:\Users\tlima\Downloads\SIMP-PE\data\extracted_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(extracted_index, f, ensure_ascii=False, indent=2)

    total_chars = sum(d["content_char_count"] for d in extracted_index)
    print(f"\nExtração concluída!")
    print(f"Total de documentos processados: {len(extracted_index)}")
    print(f"Volume total de texto extraído: {total_chars:,} caracteres (~{total_chars//5:,} palavras).")

if __name__ == "__main__":
    run_extraction()
