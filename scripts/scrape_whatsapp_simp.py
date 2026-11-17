import os
import sys
import time
import json
import re
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_DIR = Path(r"c:\Users\tlima\Downloads\SIMP-PE")
DATA_DIR = BASE_DIR / "data"
PROFILE_DIR = BASE_DIR / "whatsapp_profile"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

def setup_driver():
    options = Options()
    # Usar perfil persistente para salvar o login do WhatsApp
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # Evitar detecção como bot simples
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    print("Inicializando o navegador Google Chrome para o WhatsApp Web...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def wait_for_whatsapp_login(driver, timeout=120):
    print("Acessando https://web.whatsapp.com...")
    driver.get("https://web.whatsapp.com")
    print("\n" + "="*60)
    print(" ATENÇÃO:")
    print(" Se for a primeira vez nesta janela, por favor escaneie")
    print(" o QR Code com o aplicativo do WhatsApp no seu celular.")
    print(" Aguardando você se conectar à tela principal...")
    print("="*60 + "\n")

    # Espera até a caixa de busca ou a lista de conversas aparecer
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Procura por elementos típicos do WhatsApp logado
            search_boxes = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true'][role='textbox'], div[data-tab='3'], #side")
            if search_boxes and any(box.is_displayed() for box in search_boxes):
                print("WhatsApp Web conectado com sucesso!")
                time.sleep(3)
                return True
        except Exception:
            pass
        time.sleep(2)

    print("Tempo limite de espera pelo login excedido.")
    return False

def search_simp_chats(driver, query="SIMP"):
    print(f"\nPesquisando por chats/grupos contendo: '{query}'...")
    try:
        # Localiza a caixa de busca de chats
        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][role='textbox'], div[data-tab='3']"))
        )
        search_box.click()
        time.sleep(1)
        # Limpa busca anterior se houver
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        # Digita a pesquisa
        search_box.send_keys(query)
        time.sleep(4)
    except Exception as e:
        print(f"Erro ao localizar campo de busca: {e}")
        return []

    # Localiza a lista lateral de chats
    chat_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem'], div[data-testid='cell-frame-container'], div[data-testid='chat-list'] > div")
    print(f"Encontrados elementos de conversas na lista lateral: {len(chat_elements)}")

    simp_chats = []
    for el in chat_elements:
        try:
            text = el.text
            if query.lower() in text.lower():
                # Encontra o título específico se possível
                title_elem = el.find_elements(By.CSS_SELECTOR, "span[title]")
                title = title_elem[0].get_attribute("title") if title_elem else text.split("\n")[0]
                if query.lower() in title.lower():
                    simp_chats.append((title, el))
        except Exception:
            continue

    print(f"Grupos/Chats do SIMP identificados ({len(simp_chats)}):")
    for title, _ in simp_chats:
        print(f"  - {title}")

    return simp_chats

def extract_messages_from_active_chat(driver, chat_title, max_scrolls=20):
    print(f"\nExtraindo mensagens do grupo: '{chat_title}'...")
    
    # Rolar para cima para carregar histórico anterior
    try:
        # Localiza o contêiner de mensagens
        conversation_panel = driver.find_element(By.CSS_SELECTOR, "div[data-testid='conversation-panel-messages'], div[role='application']")
        
        print(f"Carregando histórico anterior (rolando {max_scrolls} vezes para cima)...")
        for s in range(max_scrolls):
            driver.execute_script("arguments[0].scrollTop = 0;", conversation_panel)
            time.sleep(1.2)
    except Exception as e:
        print(f"Aviso ao rolar mensagens: {e}")

    # Agora coleta todas as mensagens visíveis
    # No WhatsApp Web, cada mensagem tem o atributo 'data-pre-plain-text' com data/hora e remetente
    message_nodes = driver.find_elements(By.CSS_SELECTOR, "div[data-pre-plain-text]")
    print(f"Mensagens encontradas no painel: {len(message_nodes)}")

    extracted_msgs = []
    pattern = re.compile(r"\[(\d{1,2}:\d{1,2}(?::\d{1,2})?)[,\s]+(\d{1,2}/\d{1,2}/\d{2,4})\]\s*([^:]+):")

    for node in message_nodes:
        try:
            pre_text = node.get_attribute("data-pre-plain-text") or ""
            # Texto da mensagem
            text_nodes = node.find_elements(By.CSS_SELECTOR, "span.selectable-text")
            msg_text = "\n".join([tn.text for tn in text_nodes if tn.text.strip()])

            # Verifica se há imagens (ex: prints de erro)
            img_nodes = node.find_elements(By.CSS_SELECTOR, "img[src*='blob:'], img[src*='whatsapp']")
            has_images = len(img_nodes) > 0

            time_str, date_str, sender_str = "", "", ""
            match = pattern.search(pre_text)
            if match:
                time_str, date_str, sender_str = match.groups()
                sender_str = sender_str.strip()
            else:
                sender_str = pre_text.strip(" []:")

            if msg_text or has_images:
                extracted_msgs.append({
                    "date": date_str,
                    "time": time_str,
                    "sender": sender_str,
                    "text": msg_text,
                    "has_image": has_images
                })
        except Exception:
            continue

    print(f"Mensagens extraídas com sucesso de '{chat_title}': {len(extracted_msgs)}")
    return extracted_msgs

def run_scraper():
    driver = None
    try:
        driver = setup_driver()
        logged_in = wait_for_whatsapp_login(driver, timeout=180)
        if not logged_in:
            print("Não foi possível continuar sem a autenticação no WhatsApp Web.")
            return

        chats = search_simp_chats(driver, query="SIMP")
        if not chats:
            print("Nenhum chat com o nome 'SIMP' foi retornado na busca inicial.")
            print("Tentando buscar por 'SIMP-PE'...")
            chats = search_simp_chats(driver, query="SIMP-PE")

        all_chats_data = []

        for title, element in chats:
            try:
                print(f"\nAbrindo chat: {title}")
                # Clica no chat para abrir
                element.click()
                time.sleep(3)
                
                messages = extract_messages_from_active_chat(driver, title, max_scrolls=25)
                all_chats_data.append({
                    "chat_title": title,
                    "total_messages": len(messages),
                    "messages": messages
                })
            except Exception as e:
                print(f"Erro ao processar o chat '{title}': {e}")

        # Salva o resultado
        output_file = DATA_DIR / "whatsapp_scraped_raw.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_chats_data, f, ensure_ascii=False, indent=2)

        print("\n" + "="*60)
        print(f" EXTRAÇÃO FINALIZADA COM SUCESSO!")
        print(f" Total de grupos processados: {len(all_chats_data)}")
        total_msgs = sum(c['total_messages'] for c in all_chats_data)
        print(f" Total de mensagens capturadas: {total_msgs}")
        print(f" Arquivo salvo em: {output_file}")
        print("="*60 + "\n")

        # Integra automaticamente com a base de conhecimento
        update_knowledge_base(all_chats_data)

    except Exception as e:
        print(f"Erro inesperado durante a execução: {e}")
    finally:
        if driver:
            print("Encerrando navegador...")
            try:
                driver.quit()
            except Exception:
                pass

def update_knowledge_base(all_chats_data):
    kb_path = DATA_DIR / "troubleshooting_kb.json"
    if not kb_path.exists():
        return

    with open(kb_path, "r", encoding="utf-8") as f:
        kb = json.load(f)

    if "comunidade_whatsapp" not in kb["categories"]:
        kb["categories"]["comunidade_whatsapp"] = {
            "title": "Comunidade de Usuários WhatsApp (SIMP-PE)",
            "keywords": ["whatsapp", "dúvida", "problema", "erro", "relato", "solução"],
            "docs": [],
            "issues": []
        }

    wa_cat = kb["categories"]["comunidade_whatsapp"]
    existing_titles = {iss["title"] for iss in wa_cat["issues"]}

    keywords_prob = ["erro", "não consigo", "travou", "como faz", "pje", "bry", "csmp", "substitui", "desapareceu", "sumiu", "bloqueado"]
    keywords_sol = ["resolvi", "basta", "tem que", "só ir", "consegui", "a solução é", "faça", "orientação"]

    new_count = 0
    for chat in all_chats_data:
        msgs = chat["messages"]
        for i, msg in enumerate(msgs):
            txt = msg["text"].lower()
            if any(kp in txt for kp in keywords_prob) and len(msg["text"]) > 20:
                # Procura resposta nas próximas mensagens
                solutions = []
                for j in range(i + 1, min(i + 5, len(msgs))):
                    next_txt = msgs[j]["text"].lower()
                    if any(ks in next_txt for ks in keywords_sol) and len(msgs[j]["text"]) > 15:
                        solutions.append(f"{msgs[j]['sender']}: {msgs[j]['text']}")

                if solutions:
                    title_clean = msg["text"].split("\n")[0][:80]
                    issue_title = f"[{chat['chat_title']}] {title_clean}"
                    if issue_title not in existing_titles:
                        wa_cat["issues"].append({
                            "id": f"WAP-{len(wa_cat['issues']) + 1:03d}",
                            "title": issue_title,
                            "category": "Comunidade WhatsApp",
                            "symptoms": [msg["text"][:200]],
                            "cause": f"Problema ou dúvida reportada por {msg['sender']} no grupo {chat['chat_title']}.",
                            "solution": "\n\n".join(solutions),
                            "ref": f"WhatsApp {chat['chat_title']} ({msg['date']})"
                        })
                        existing_titles.add(issue_title)
                        new_count += 1

    with open(kb_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

    print(f"Base de conhecimento atualizada com {new_count} novos casos reais do WhatsApp!")

if __name__ == "__main__":
    run_scraper()
