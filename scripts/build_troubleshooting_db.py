import json
import os
import re
from pathlib import Path

BASE_DIR = Path(r"c:\Users\tlima\Downloads\SIMP-PE")
DATA_DIR = BASE_DIR / "data"
EXTRACTED_DIR = DATA_DIR / "extracted"

def build_knowledge_base():
    with open(DATA_DIR / "extracted_index.json", "r", encoding="utf-8") as f:
        extracted_index = json.load(f)

    print(f"Indexando {len(extracted_index)} documentos extraídos...")

    # Categorias do SIMP-PE
    categories = {
        "acesso_perfis": {
            "title": "Acesso, Autenticação, Perfis e Substituições",
            "keywords": ["login", "senha", "perfil", "perfis", "substitui", "lotação", "usuário", "permissão", "acesso", "mastiff"],
            "docs": [],
            "issues": [
                {
                    "id": "AC-01",
                    "title": "Processo não aparece na caixa de trabalho do Membro/Servidor substituto",
                    "category": "Acesso e Substituições",
                    "symptoms": ["Membro substituto não visualiza os processos da Promotoria substituída", "Caixa de entrada vazia", "Erro de atribuição temporária"],
                    "cause": "Tabela de substituição não configurada com período de vigência ativo ou perfil de substituição sem vínculo à unidade orgânica correta.",
                    "solution": "1. Acesse o módulo de Configurações Administrativas > Tabela de Substituições.\n2. Verifique se o vínculo entre o Membro Titular e o Membro Substituto está cadastrado com as datas de início e término correspondentes ao ato formal da PGJ/CGMP.\n3. Certifique-se de que a opção 'Visualizar acervo e processos em andamento' está habilitada no perfil temporário.\n4. Solicite ao usuário realizar logout e login novamente para recarregar o token de permissões na sessão.",
                    "ref": "Manual de Configuração do Sistema SIMP / Tabela de Substituição no Sistema SIMP"
                },
                {
                    "id": "AC-02",
                    "title": "Erro de autenticação ou 'Acesso Negado' ao tentar acessar módulo específico",
                    "category": "Acesso e Perfis",
                    "symptoms": ["Mensagem 'Usuário não autorizado a realizar esta operação'", "Botão ou menu indisponível"],
                    "cause": "Perfil de acesso atribuído ao cargo não possui permissão concedida na matriz de segurança (Mastiff/IAM do MPPE).",
                    "solution": "1. Verifique a lotação ativa do servidor/membro no módulo Gestão de Pessoal e Documentos.\n2. Caso o usuário possua múltiplas lotações (ex: Promotoria de Origem e Central de Inquéritos), orientar a trocar a lotação ativa no menu superior direito do SIMP.\n3. Se persistir, o gestor da unidade deve abrir chamado solicitando a inclusão do perfil correspondente na DEMSI/DTI.",
                    "ref": "Tutorial: Configuração de Usuário no Ecossistema SIMP"
                }
            ]
        },
        "protocolo": {
            "title": "Protocolo, Triagem e Entrada de Documentos",
            "keywords": ["protocolo", "triagem", "autua", "notícia de fato", "recebimento", "apensamento", "desentranhamento"],
            "docs": [],
            "issues": [
                {
                    "id": "PR-01",
                    "title": "Erro ao registrar Protocolo ou autuar Notícia de Fato inicial",
                    "category": "Protocolo",
                    "symptoms": ["Campos obrigatórios bloqueados", "Erro 'Parte/Interessado não localizado no cadastro'", "Falha na validação de CPF/CNPJ"],
                    "cause": "Tentativa de registro sem preenchimento de campos qualificadores essenciais ou duplicidade cadastral de pessoa física/jurídica.",
                    "solution": "1. No módulo Protocolo > Atendimento ao Público / Notícia de Fato, realize a busca prévia de partes no Cadastro Básico Unificado.\n2. Caso a parte não exista, efetue o pré-cadastro com nome completo, documento (CPF/CNPJ) e endereço.\n3. Se o interessado for anônimo, marque a flag 'Interessado Anônimo/Sigiloso', justificando nos termos da Resolução CSMP.\n4. Confirme a autuação e certifique-se da geração do número único de protocolo.",
                    "ref": "Fluxo SIMP4 Protocolo 1ª Instância / Fluxo Atendimento ao Público (NF)"
                },
                {
                    "id": "PR-02",
                    "title": "Dificuldade em desmembrar ou apensar protocolos / autos",
                    "category": "Protocolo",
                    "symptoms": ["Erro 'Operação não permitida no estado atual do procedimento'", "Autos bloqueados"],
                    "cause": "Procedimento com pendência de movimentação em aberto ou em trânsito de distribuição.",
                    "solution": "1. Verifique se há minuta não assinada ou remessa pendente de confirmação no protocolo.\n2. Conclua ou cancele a minuta pendente.\n3. Acesse 'Operações de Autos' > 'Apensar/Desapensar' ou 'Desmembrar', informe a justificativa e anexe o despacho correspondente.",
                    "ref": "Esquema de Movimentações Possíveis - Protocolo SIMP"
                }
            ]
        },
        "extrajudicial": {
            "title": "Módulo Extrajudicial (NF, PP, IC, PA, TAC)",
            "keywords": ["extrajudicial", "notícia de fato", "inquérito civil", "procedimento preparatório", "procedimento administrativo", "tac", "prorrogação", "csmp"],
            "docs": [],
            "issues": [
                {
                    "id": "EX-01",
                    "title": "Prazo da Notícia de Fato expirando sem conseguir converter em PP ou IC",
                    "category": "Extrajudicial",
                    "symptoms": ["Notícia de Fato atinge os 30 dias regulamentares", "Sistema não permite movimentação sem despacho de prorrogação ou conversão"],
                    "cause": "Regras da Resolução CSMP nº 03/2019 e Resolução PGJ exigem ato formal fundamentado de prorrogação única (até 90 dias) ou despacho de instauração de PP/IC.",
                    "solution": "1. Abra a Notícia de Fato na caixa de trabalho da Promotoria.\n2. Clique em 'Elaborar Documento' > selecione o modelo 'Portaria de Instauração de Procedimento Preparatório' ou 'Inquérito Civil' (ou 'Despacho de Prorrogação de NF').\n3. Redija os termos, assine digitalmente via Escriba/BRY.\n4. Ao assinar a Portaria, acesse 'Movimentações' > 'Evoluir Procedimento' e selecione o tipo destino (PP ou IC). O sistema atualizará a classe e recalculará os contadores de prazo.",
                    "ref": "Resolução CSMP 03/2019 / Análise do Módulo Extrajudicial no Sistema SIMP"
                },
                {
                    "id": "EX-02",
                    "title": "Erro ao remeter Inquérito Civil arquivado para homologação do CSMP",
                    "category": "Extrajudicial",
                    "symptoms": ["Botão de remessa ao Conselho Superior indisponível", "Erro 'Falta certidão de intimação dos interessados'"],
                    "cause": "Arquivamento de IC/PP requer comprovação de notificação/comunicação das partes/noticiante para recurso no prazo de 10 dias.",
                    "solution": "1. Junte aos autos a certidão ou comprovante de ciência/notificação do denunciante/interessado sobre a promoção de arquivamento.\n2. Certifique o decurso do prazo recursal regulamentar de 10 dias.\n3. No menu do procedimento, selecione 'Promover Remessa' > Destino: 'Conselho Superior do Ministério Público (CSMP)'. O procedimento será encaminhado à fila de distribuição do CSMP.",
                    "ref": "Manual SIMP - Módulo Extrajudicial / Resolução CSMP"
                }
            ]
        },
        "judicial": {
            "title": "Módulo Judicial e Integração PJe / TJPE",
            "keywords": ["judicial", "pje", "tribunal de justiça", "tjpe", "intimação", "prazo", "ciência", "denúncia", "citação", "mni"],
            "docs": [],
            "issues": [
                {
                    "id": "JD-01",
                    "title": "Intimações do PJe/TJPE não aparecem no SIMP ou erro de sincronização MNI",
                    "category": "Judicial e Integração PJe",
                    "symptoms": ["Novas intimações eletrônicas expedidas no PJe não são listadas na caixa judicial do SIMP", "Falha no serviço MNI"],
                    "cause": "Instabilidade momentânea no WebService de integração MNI do TJPE ou divergência na parametrização do Código de Jurisdição/Vara no SIMP.",
                    "solution": "1. Acesse o menu 'Judicial' > 'Sincronizar com PJe' para forçar uma consulta manual ao barramento.\n2. Verifique se o órgão de atuação está com o código de jurisdição e serventia cadastrado de acordo com a tabela unificada (Tabelas Básicas PJe / Promotorias para Varas).\n3. Caso o PJe do TJPE esteja fora do ar ou com certificado expirado, acione o suporte da DEMSI para verificar o status do webhook MNI.",
                    "ref": "Fluxo Judicial no Sistema SIMP / Códigos Jurisdição 1G e 2G / Integração Órgãos Externos"
                },
                {
                    "id": "JD-02",
                    "title": "Erro ao devolver autos com Manifestação ao PJe pelo SIMP",
                    "category": "Judicial",
                    "symptoms": ["Erro 'Tamanho do arquivo excede o limite permitido pelo PJe'", "Erro de assinatura no protocolo externo"],
                    "cause": "O Tribunal de Justiça impõe limites estritos de tamanho (normalmente arquivos individuais de até 5MB a 10MB) e formato exclusivo PDF/A, ou falha de token de comunicação.",
                    "solution": "1. No módulo de juntada de documentos, verifique o tamanho dos arquivos anexos.\n2. Caso haja PDFs grandes, utilize a ferramenta de otimização/compressão de PDF disponível no MPPE ou divida os documentos em volumes fracionados de até 5MB.\n3. Certifique-se de que a manifestação principal foi assinada digitalmente com certificado válido antes do envio.",
                    "ref": "Manual de Integração de Sistemas Externos / Fluxo Processos Judiciais 1ª Instância"
                }
            ]
        },
        "distribuicao": {
            "title": "Distribuição, Regras e Contadores",
            "keywords": ["distribuição", "contador", "sorteio", "compensação", "central de inquéritos", "cinq", "plantão", "impedimento", "suspeição"],
            "docs": [],
            "issues": [
                {
                    "id": "DS-01",
                    "title": "Divergência ou desbalanceamento no contador de distribuição entre membros",
                    "category": "Distribuição",
                    "symptoms": ["Um promotor recebe significativamente mais processos que outro na mesma unidade", "Contador zerado ou travado"],
                    "cause": "Regras de peso por matéria (Cível, Família, Fazenda, Tribunal do Júri) ou lançamentos incorretos de licença/compensação no perfil do membro.",
                    "solution": "1. Acesse o painel de 'Gestão de Distribuição' > 'Relatório de Contadores'.\n2. Verifique o peso atribuído a cada classe processual de acordo com o Provimento da CGMP/Resolução PGJ.\n3. Confira se os afastamentos (férias, licenças) dos membros foram registrados no sistema com compensação automática ativada.\n4. Caso necessário, o administrador da distribuição pode executar o ajuste de compensação manual justificando em ata.",
                    "ref": "Distribuição - Contadores SIMP / Análise Consolidada e Proposta de Contadores"
                },
                {
                    "id": "DS-02",
                    "title": "Processo distribuído para Promotor com Impedimento ou Suspeição",
                    "category": "Distribuição",
                    "symptoms": ["Membro recebe feito de parte impedida ou processo em que já atuou em outra qualidade"],
                    "cause": "Falta de cadastro prévio do impedimento no perfil do membro ou distribuição por prevenção equivocada.",
                    "solution": "1. O Membro deve despachar nos autos fundamentando o impedimento/suspeição com base na legislação (CPC/CPP).\n2. Na tela de movimentação, selecione a opção 'Declarar Impedimento/Suspeição'.\n3. O sistema devolverá o procedimento para a fila de redistribuição da Central/Secretaria, compensando automaticamente 1 ponto no contador do membro e redistribuindo para o substituto legal.",
                    "ref": "Resoluções das Centrais de Inquéritos / Regras de Distribuição SIMP4"
                }
            ]
        },
        "escriba_assinatura": {
            "title": "Escriba, Editor de Textos e Assinatura Digital (BRY)",
            "keywords": ["escriba", "assinatura", "bry", "certificado", "token", "digital", "pdf", "modelo", "variável"],
            "docs": [],
            "issues": [
                {
                    "id": "ES-01",
                    "title": "Erro ao assinar documento digitalmente: 'Falha no componente BRY' ou 'Certificado não detectado'",
                    "category": "Escriba e Assinatura Digital",
                    "symptoms": ["Janela de assinatura trava", "Mensagem 'Não foi possível conectar ao integrador de assinatura BRY'"],
                    "cause": "Serviço local do BRY WebSigner desatualizado, serviço parado no Windows ou bloqueio de porta no navegador.",
                    "solution": "1. Verifique se o aplicativo BRY WebSigner / Extensão do navegador está em execução na barra de tarefas do Windows (ícone próximo ao relógio).\n2. Se o ícone não estiver presente, abra o Menu Iniciar > digite 'Bry WebSigner' e execute o programa.\n3. Recarregue a página do SIMP (Ctrl + F5).\n4. Se utilizar Token físico USB, retire e reconecte em outra porta USB e confirme se o cartão/token está lido pelo Safenet/SafeSign.",
                    "ref": "Manual Escriba MPPE / Bry Simp Documentação Técnica"
                },
                {
                    "id": "ES-02",
                    "title": "Variáveis do modelo de documento do Escriba não carregam os dados dos autos",
                    "category": "Escriba",
                    "symptoms": ["Campos como {{nome_interessado}}, {{numero_processo}} ficam em branco ou com código literal"],
                    "cause": "Variável cadastrada incorretamente na base de modelos ou dados não preenchidos na autuação do procedimento.",
                    "solution": "1. Verifique na autuação do procedimento se as partes estão devidamente qualificadas com nome e papéis definidos (ex: Noticiante, Noticiado, Autor, Réu).\n2. No editor do Escriba, clique no menu 'Inserir Variável' e utilize a lista oficial de tags do sistema em vez de digitar manualmente o texto da variável.",
                    "ref": "Manual Escriba MPPE / Projeto Documental SIMP"
                }
            ]
        }
    }

    # Agora vamos varrer os arquivos de texto extraídos e associar trechos relevantes
    for item in extracted_index:
        filename = item["filename"]
        extracted_rel = item["extracted_file"]
        ext_path = BASE_DIR / extracted_rel

        if not ext_path.exists():
            continue

        with open(ext_path, "r", encoding="utf-8", errors="replace") as f_in:
            text = f_in.read()

        text_lower = text.lower()
        for cat_key, cat_data in categories.items():
            matches = sum(text_lower.count(kw) for kw in cat_data["keywords"])
            if matches > 10:
                cat_data["docs"].append({
                    "filename": filename,
                    "original_path": item["original_path"],
                    "relevance_score": matches,
                    "size_mb": item["size_mb"]
                })

    # Ordenar docs de cada categoria por relevância
    for cat_key, cat_data in categories.items():
        cat_data["docs"].sort(key=lambda x: x["relevance_score"], reverse=True)
        cat_data["docs"] = cat_data["docs"][:15] # Top 15 mais relevantes

    kb_output = {
        "version": "1.0",
        "system_name": "SIMP-PE (Sistema Integrado do Ministério Público de Pernambuco)",
        "total_documents_indexed": len(extracted_index),
        "categories": categories
    }

    with open(DATA_DIR / "troubleshooting_kb.json", "w", encoding="utf-8") as f_out:
        json.dump(kb_output, f_out, ensure_ascii=False, indent=2)

    print(f"Base de conhecimento de Troubleshooting gerada com sucesso em: {DATA_DIR / 'troubleshooting_kb.json'}")

if __name__ == "__main__":
    build_knowledge_base()
