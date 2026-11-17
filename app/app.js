// Estado da aplicação
let knowledgeBase = null;
let allIssues = [];
let activeCategory = 'all';
let searchQuery = '';

// Elementos do DOM
const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const categorySelect = document.getElementById('categorySelect');
const issuesList = document.getElementById('issuesList');
const resultsCount = document.getElementById('resultsCount');
const modulesList = document.getElementById('modulesList');
const manualsList = document.getElementById('manualsList');
const tabButtons = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');
const tagButtons = document.querySelectorAll('.tag-btn');

// Inicialização
document.addEventListener('DOMContentLoaded', async () => {
  setupTabs();
  setupSearch();
  setupTags();
  setupDropzone();
  await loadData();
});

// Alternar abas
function setupTabs() {
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.dataset.tab;
      tabButtons.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const targetPane = document.getElementById(`tab-${tabId}`);
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

// Configurar Busca e Filtros
function setupSearch() {
  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value.trim().toLowerCase();
    clearSearchBtn.style.display = searchQuery ? 'block' : 'none';
    renderIssues();
  });

  clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    searchQuery = '';
    clearSearchBtn.style.display = 'none';
    renderIssues();
  });

  categorySelect.addEventListener('change', (e) => {
    activeCategory = e.target.value;
    renderIssues();
  });
}

// Configurar tags rápidas
function setupTags() {
  tagButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const query = btn.dataset.query;
      searchInput.value = query;
      searchQuery = query.toLowerCase();
      clearSearchBtn.style.display = 'block';
      
      // Ir para aba de troubleshooting
      const troubleTab = document.querySelector('[data-tab="troubleshooting"]');
      if (troubleTab) troubleTab.click();

      renderIssues();
    });
  });
}

// Carregar dados da Base de Conhecimento
async function loadData() {
  try {
    const res = await fetch('../data/troubleshooting_kb.json');
    if (!res.ok) throw new Error('Não foi possível carregar troubleshooting_kb.json');
    knowledgeBase = await res.json();
  } catch (err) {
    console.warn('Carregando base padrão embutida:', err);
    knowledgeBase = getDefaultKnowledgeBase();
  }

  // Achatar todos os issues em um array único
  allIssues = [];
  if (knowledgeBase && knowledgeBase.categories) {
    Object.values(knowledgeBase.categories).forEach(cat => {
      if (cat.issues) {
        cat.issues.forEach(iss => allIssues.push(iss));
      }
    });
  }

  renderIssues();
  renderModules();
  renderManuals();
}

// Renderizar lista de issues
function renderIssues() {
  if (!issuesList) return;

  const filtered = allIssues.filter(iss => {
    // Filtro por categoria
    if (activeCategory !== 'all' && iss.category !== activeCategory) {
      return false;
    }

    // Filtro por busca
    if (!searchQuery) return true;

    const fullText = [
      iss.title,
      iss.category,
      iss.cause,
      iss.solution,
      iss.ref,
      ...(iss.symptoms || [])
    ].join(' ').toLowerCase();

    return fullText.includes(searchQuery);
  });

  resultsCount.textContent = `${filtered.length} problema(s) encontrado(s)`;

  if (filtered.length === 0) {
    issuesList.innerHTML = `
      <div style="text-align: center; padding: 3rem; background: #fff; border-radius: 8px; border: 1px solid #e2e8f0;">
        <p style="font-size: 1.1rem; color: #475569; margin-bottom: 0.5rem;">Nenhuma solução encontrada para "<strong>${escapeHtml(searchQuery)}</strong>"</p>
        <p style="font-size: 0.9rem; color: #94a3b8;">Tente pesquisar com termos mais gerais, como "PJe", "BRY", "distribuição", "acesso" ou veja os módulos ao lado.</p>
      </div>
    `;
    return;
  }

  issuesList.innerHTML = filtered.map(iss => {
    const symptomsHtml = iss.symptoms && iss.symptoms.length
      ? `<div class="issue-symptoms"><strong>Sintomas relatados:</strong> ${iss.symptoms.map(s => escapeHtml(s)).join(' &bull; ')}</div>`
      : '';

    return `
      <article class="issue-card">
        <div class="card-top">
          <span class="issue-id">${escapeHtml(iss.id || 'INC')}</span>
          <span class="issue-badge">${escapeHtml(iss.category || 'Geral')}</span>
        </div>
        <h3 class="issue-title">${escapeHtml(iss.title)}</h3>
        ${symptomsHtml}
        <div class="issue-cause"><strong>Causa provável:</strong> ${escapeHtml(iss.cause)}</div>
        <div class="issue-solution-box">
          <div class="solution-header">
            <svg style="width: 16px; height: 16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
            Procedimento de Resolução Passo a Passo:
          </div>
          <div class="solution-steps">${escapeHtml(iss.solution)}</div>
        </div>
        ${iss.ref ? `<div class="issue-ref"><strong>Documento de Referência:</strong> ${escapeHtml(iss.ref)}</div>` : ''}
      </article>
    `;
  }).join('');
}

// Renderizar Módulos
function renderModules() {
  if (!modulesList || !knowledgeBase || !knowledgeBase.categories) return;

  modulesList.innerHTML = Object.entries(knowledgeBase.categories).map(([key, cat]) => {
    const kwBadges = (cat.keywords || []).slice(0, 6).map(kw => `<span class="kw-badge">${escapeHtml(kw)}</span>`).join('');
    const docsCount = cat.docs ? cat.docs.length : 0;
    const issuesCount = cat.issues ? cat.issues.length : 0;

    return `
      <div class="module-card">
        <h4>${escapeHtml(cat.title)}</h4>
        <p>Base com ${issuesCount} problema(s) mapeado(s) e ${docsCount} documento(s) associado(s).</p>
        <div class="module-keywords">${kwBadges}</div>
        <button class="primary-btn" style="font-size: 0.8rem; padding: 0.4rem 0.8rem;" onclick="filterByCategory('${escapeHtml(cat.issues && cat.issues[0] ? cat.issues[0].category : 'all')}')">Ver Problemas Deste Módulo</button>
      </div>
    `;
  }).join('');
}

window.filterByCategory = function(categoryName) {
  categorySelect.value = categoryName;
  activeCategory = categoryName;
  const troubleTab = document.querySelector('[data-tab="troubleshooting"]');
  if (troubleTab) troubleTab.click();
  renderIssues();
};

// Renderizar Manuais
function renderManuals() {
  if (!manualsList) return;

  const keyManuals = [
    { name: "Manual do Sistema SIMP4 (Versão Atualizada)", category: "Manual Oficial Completo", desc: "Guia completo de navegação, módulos processuais, perfis e configurações gerais do SIMP.", size: "56.12 MB" },
    { name: "Fluxos de Procedimentos Judiciais 1ª e 2ª Instâncias", category: "Fluxos Operacionais", desc: "Mapeamento completo do trâmite de autos, manifestações ministeriais, prazos e ciência.", size: "1.02 MB" },
    { name: "Fluxo de Atendimento ao Público e Notícia de Fato (NF)", category: "Extrajudicial", desc: "Procedimento operacional padrão para entrada, triagem, declínio e evolução de Notícias de Fato.", size: "0.76 MB" },
    { name: "Manual de Integração de Sistemas Externos e PJe / TJPE", category: "Integração MNI", desc: "Instruções de interoperabilidade com o Tribunal de Justiça de Pernambuco e Justiça Eleitoral.", size: "3.20 MB" },
    { name: "Manual do Editor Escriba e Assinador Digital BRY", category: "Escriba & Assinatura", desc: "Configuração do plugin BRY WebSigner, modelos de minutas e certificados digitais A1/A3.", size: "4.79 MB" },
    { name: "Manual de Configuração e Tabela de Substituições do MPPE", category: "Administração", desc: "Regras de negócio de substituição automática, acervo em transição e contadores de distribuição.", size: "7.17 MB" }
  ];

  manualsList.innerHTML = keyManuals.map(man => `
    <div class="manual-item">
      <div>
        <div class="manual-name">${escapeHtml(man.name)}</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 2px;">${escapeHtml(man.desc)}</div>
      </div>
      <div class="manual-meta" style="text-align: right;">
        <span class="issue-badge">${escapeHtml(man.category)}</span>
        <div style="margin-top: 4px;">${escapeHtml(man.size)}</div>
      </div>
    </div>
  `).join('');
}

// Ingestão de WhatsApp
function setupDropzone() {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const processBtn = document.getElementById('processTextBtn');
  const directTextInput = document.getElementById('directTextInput');
  const feedback = document.getElementById('importFeedback');

  if (!dropzone || !fileInput) return;

  dropzone.addEventListener('click', () => fileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#004d99';
    dropzone.style.background = '#f0f7ff';
  });

  dropzone.addEventListener('dragleave', () => {
    dropzone.style.borderColor = '#94a3b8';
    dropzone.style.background = '#fafafa';
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#94a3b8';
    dropzone.style.background = '#fafafa';
    if (e.dataTransfer.files.length > 0) {
      handleChatFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleChatFile(e.target.files[0]);
    }
  });

  if (processBtn && directTextInput) {
    processBtn.addEventListener('click', () => {
      const text = directTextInput.value.trim();
      if (!text) {
        alert('Por favor, cole o texto de conversas do WhatsApp para processar.');
        return;
      }
      processChatContent(text, 'Texto Colado Manualmente');
    });
  }
}

function handleChatFile(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    const text = e.target.result;
    processChatContent(text, file.name);
  };
  reader.readAsText(file);
}

function processChatContent(rawText, sourceName) {
  const feedback = document.getElementById('importFeedback');
  const lines = rawText.split('\n');
  let extractedCount = 0;

  // Heurística para capturar mensagens com dúvidas ou soluções
  const keywordsTrigger = ['erro', 'problema', 'não consigo', 'ajuda', 'como faz', 'travou', 'pje', 'bry', 'csmp', 'substitui'];
  const solutionTriggers = ['resolvi', 'consegui', 'basta', 'tem que', 'só ir em', 'a solução é', 'orientação'];

  // Bloco simples de exemplo de extração
  const newIssue = {
    id: `WA-${String(allIssues.length + 1).padStart(2, '0')}`,
    title: `Dúvida importada de ${sourceName}: Registro da Comunidade`,
    category: "Comunidade WhatsApp",
    symptoms: ["Mensagem reportada no grupo do WhatsApp SIMP-PE"],
    cause: "Relato direto de usuário da comunidade durante a rotina operacional.",
    solution: rawText.length > 300 ? rawText.substring(0, 300) + '...' : rawText,
    ref: `Comunidade SIMP WhatsApp (${sourceName})`
  };

  allIssues.unshift(newIssue);
  extractedCount = 1;

  if (feedback) {
    feedback.style.display = 'block';
    feedback.innerHTML = `<strong>Sucesso!</strong> O histórico de <strong>${escapeHtml(sourceName)}</strong> foi analisado e adicionado à base de troubleshooting ativa.`;
  }

  renderIssues();
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Fallback caso abra via file://
function getDefaultKnowledgeBase() {
  return {
    categories: {
      acesso: {
        title: "Acesso e Perfis",
        issues: [
          {
            id: "AC-01",
            title: "Processo não aparece na caixa do Membro/Servidor substituto",
            category: "Acesso e Substituições",
            symptoms: ["Membro substituto não visualiza os processos"],
            cause: "Tabela de substituição não configurada com período de vigência ativo.",
            solution: "1. Acesse Configurações > Tabela de Substituições.\n2. Verifique o vínculo de datas.\n3. Faça logout e login novamente.",
            ref: "Manual de Configuração SIMP"
          }
        ]
      }
    }
  };
}
