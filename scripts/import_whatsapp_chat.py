import os
import sys
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
KB_PATH = DATA_DIR / "troubleshooting_kb.json"

def parse_whatsapp_file(file_path):
    print(f"Processando arquivo de conversa: {file_path}")
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    # Regex comum do WhatsApp no Brasil: [dd/mm/aaaa, hh:mm:ss] Nome: Mensagem ou dd/mm/aaaa hh:mm - Nome: Mensagem
    pattern = re.compile(r"^\[?(\d{1,2}/\d{1,2}/\d{2,4})[,\s]+(\d{1,2}:\d{1,2}(?::\d{1,2})?)\]?\s*(?:-\s*)?([^:]+):\s*(.*)$")

    messages = []
    current_msg = None

    for line in lines:
        line_clean = line.strip()
        match = pattern.match(line_clean)
        if match:
            if current_msg:
                messages.append(current_msg)
            date, time, sender, text = match.groups()
            current_msg = {
                "date": date,
                "time": time,
                "sender": sender.strip(),
                "text": text.strip()
            }
        else:
            if current_msg:
                current_msg["text"] += "\n" + line_clean

    if current_msg:
        messages.append(current_msg)

    print(f"Total de mensagens identificadas: {len(messages)}")
    return messages

def extract_qa_pairs(messages):
    keywords_problem = [
        "erro", "falha", "não consigo", "travou", "não abre", "bloqueado",
        "pje", "bry", "certificado", "substitui", "csmp", "notícia de fato",
        "distribuição", "contador", "autuação", "escriba", "sumiu", "alguém sabe"
    ]
    keywords_solution = [
        "consegui", "resolvido", "basta", "tem que", "só ir", "a solução",
        "faça o seguinte", "atualize", "o procedimento é", "orientação da demsi"
    ]

    extracted_cases = []
    
    # Heurística de janela deslizante para pegar conversas de dúvida e resposta
    for i, msg in enumerate(messages):
        text_lower = msg["text"].lower()
        if any(kw in text_lower for kw in keywords_problem):
            # Procura respostas nas próximas 5 mensagens
            potential_solutions = []
            for j in range(i + 1, min(i + 6, len(messages))):
                next_msg = messages[j]
                next_lower = next_msg["text"].lower()
                if any(skw in next_lower for skw in keywords_solution):
                    potential_solutions.append(f"{next_msg['sender']}: {next_msg['text']}")

            if potential_solutions:
                extracted_cases.append({
                    "date": msg["date"],
                    "question_sender": msg["sender"],
                    "question": msg["text"],
                    "solutions": potential_solutions
                })

    print(f"Casos com perguntas e soluções detectadas: {len(extracted_cases)}")
    return extracted_cases

def update_kb_with_cases(cases, source_name="WhatsApp SIMP"):
    if not KB_PATH.exists():
        print(f"Base de conhecimento não encontrada em {KB_PATH}")
        return

    with open(KB_PATH, "r", encoding="utf-8") as f:
        kb = json.load(f)

    if "whatsapp_cases" not in kb["categories"]:
        kb["categories"]["whatsapp_cases"] = {
            "title": "Casos da Comunidade WhatsApp SIMP",
            "keywords": ["whatsapp", "comunidade", "caso prático", "dúvida recorrente"],
            "docs": [],
            "issues": []
        }

    wa_category = kb["categories"]["whatsapp_cases"]
    existing_ids = {iss["id"] for iss in wa_category["issues"]}

    added = 0
    for idx, c in enumerate(cases, 1):
        case_id = f"WA-{len(existing_ids) + idx:03d}"
        if case_id in existing_ids:
            continue

        title_preview = c["question"].split("\n")[0][:80]
        issue = {
            "id": case_id,
            "title": f"Dúvida Comunidade: {title_preview}...",
            "category": "Comunidade WhatsApp",
            "symptoms": [c["question"][:150] + ("..." if len(c["question"]) > 150 else "")],
            "cause": "Dúvida operacional reportada diretamente por usuário nos grupos do SIMP.",
            "solution": "\n\n".join(c["solutions"]),
            "ref": f"Histórico {source_name} ({c['date']})"
        }
        wa_category["issues"].append(issue)
        existing_ids.add(case_id)
        added += 1

    with open(KB_PATH, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

    print(f"{added} novos casos adicionados com sucesso ao troubleshooting_kb.json!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_arg = Path(sys.argv[1])
        if file_arg.exists():
            msgs = parse_whatsapp_file(file_arg)
            cases = extract_qa_pairs(msgs)
            update_kb_with_cases(cases, file_arg.name)
    else:
        print("Uso: python import_whatsapp_chat.py <caminho_do_arquivo_exportado.txt>")
        print("Dica: você também pode usar a aba de importação visual na interface web!")
