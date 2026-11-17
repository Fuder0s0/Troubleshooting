# troubleshooting SIMP-PE 🏛️

Sistema inteligente de auxílio, diagnóstico e solução de incidentes/dúvidas operacionais do **SIMP4 (Sistema Integrado do Ministério Público de Pernambuco)**.

Desenvolvido para atender membros, servidores, estagiários e equipes de suporte da **DEMSI / DTI do MPPE**, permitindo a consulta rápida a soluções de problemas, regras de negócio, fluxos processuais e integração contínua com a comunidade de usuários.

---

## 🚀 Principais Recursos

- **🔍 Busca Instantânea e Inteligente:** Pesquisa em tempo real por palavras-chave, mensagens de erro, códigos de incidente ou sintomas operacionais.
- **🛠️ Diagnóstico Passo a Passo:** Orientações detalhadas para resolução imediata de problemas em:
  - **Acesso, Perfis e Substituições:** Lotações, tabela de substituições temporárias e permissões no ecossistema (Mastiff).
  - **Protocolo e Triagem:** Autuação de procedimentos, validação de partes e apensamento/desmembramento de autos.
  - **Módulo Extrajudicial:** Prazos e evolução de Notícia de Fato (NF), Procedimento Preparatório (PP), Inquérito Civil (IC), Procedimento Administrativo (PA) e remessa homologatória ao Conselho Superior (CSMP).
  - **Módulo Judicial e PJe:** Sincronização MNI com o Tribunal de Justiça de Pernambuco (TJPE), devolução de autos com manifestação, limites de arquivos e códigos de serventia.
  - **Distribuição e Contadores:** Regras de compensação, prevenção, impedimentos, suspeições e rotinas das Centrais de Inquéritos (CINQ).
  - **Escriba e Assinatura Digital:** Configuração do componente BRY WebSigner, certificados digitais ICP-Brasil e variáveis dinâmicas de modelos.
- **📚 Acervo Documental Indexado:** Catálogo completo dos manuais oficiais, tabelas de jurisdição e resoluções normativas do MPPE.
- **💬 Ingestor da Comunidade WhatsApp:** Módulo visual e via linha de comando para importar históricos de conversas dos grupos do WhatsApp do SIMP, parseando automaticamente dúvidas recorrentes e respostas dos analistas para enriquecer a base de conhecimento.

---

## 📂 Estrutura do Repositório

```text
troubleshooting-SIMP-PE/
│
├── app/                              # Aplicação Web de Troubleshooting
│   ├── index.html                    # Interface do usuário (SPA responsiva)
│   ├── style.css                     # Estilos institucionais (MPPE)
│   ├── app.js                        # Lógica da busca, filtros e ingestão
│   └── server.py                     # Servidor HTTP local leve em Python
│
├── data/                             # Base de Conhecimento Indexada
│   ├── troubleshooting_kb.json       # Base estruturada de problemas e soluções
│   ├── catalog_raw.json              # Inventário de arquivos e documentos
│   ├── catalog_summary.json          # Sumário estatístico do acervo
│   ├── extracted_index.json          # Índice de textos e metadados extraídos
│   └── extracted/                    # Textos extraídos dos manuais e normas (3,7 MB)
│
├── scripts/                          # Pipelines de Processamento e Automação
│   ├── catalog_simp.py               # Mapeamento do acervo compartilhado
│   ├── extract_text_knowledge.py     # Extração textual de PDFs, DOCXs e normas
│   ├── build_troubleshooting_db.py   # Compilação da base de conhecimento
│   └── import_whatsapp_chat.py       # Parser de exportação dos grupos do WhatsApp
│
├── iniciar_troubleshooting.bat        # Inicializador rápido de um clique para Windows
├── .gitignore                        # Regras de exclusão de arquivos no Git
└── README.md                         # Documentação do projeto
```

---

## 💻 Como Executar Localmente

### Método 1: Duplo Clique (Recomendado para Windows)
Dê um duplo clique no arquivo:
```text
iniciar_troubleshooting.bat
```
O servidor será iniciado e a aplicação abrirá automaticamente no seu navegador padrão em `http://localhost:8080/app/`.

### Método 2: Via Terminal / Linha de Comando
```bash
python app/server.py
```

---

## 📲 Como Importar Grupos do WhatsApp

1. No aplicativo do WhatsApp (ou Web):
   - Abra o grupo da comunidade do SIMP.
   - Clique em **Mais** > **Exportar conversa** (com ou sem mídia).
2. Na aplicação web, acesse a aba **"Integração Comunidade WhatsApp"** e arraste o arquivo `.txt`.
3. Alternativamente, execute via terminal:
   ```bash
   python scripts/import_whatsapp_chat.py "caminho_da_conversa_exportada.txt"
   ```
O sistema processará o diálogo, identificará os pares de perguntas/soluções e atualizará imediatamente o catálogo de troubleshooting.

---

## 🌐 Publicação no GitHub

Para vincular este repositório à sua conta do GitHub:

```bash
# 1. Crie um repositório no GitHub com o nome: troubleshooting-SIMP-PE
# 2. No terminal desta pasta, execute:
git remote add origin https://github.com/SEU_USUARIO/troubleshooting-SIMP-PE.git
git branch -M main
git push -u origin main
```

---

### Licença e Créditos
Desenvolvido para o **Ministério Público do Estado de Pernambuco (MPPE)**.  
DEMSI / DTI.
