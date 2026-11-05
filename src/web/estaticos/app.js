/**
 * Frontend JavaScript do Citizen Assist AI.
 * Controla requisições RESTful para a Lista Encadeada no backend e manipula o DOM.
 */

const API_BASE = "";

// Estado local da interface
let servicosAtuais = [];

document.addEventListener("DOMContentLoaded", () => {
  carregarServicos();
  carregarEstatisticas();

  // Suporte a abertura direta por hash ou parâmetro de URL
  const params = new URLSearchParams(window.location.search);
  const abaParam = params.get("aba") || window.location.hash.replace("#", "");
  if (abaParam) {
    const btnAlvo = document.querySelector(`[onclick*="${abaParam}"]`);
    if (btnAlvo) btnAlvo.click();
  }
});

// ==============================================================================
// NAVEGAÇÃO DE ABAS
// ==============================================================================
function mudarAba(idAba) {
  document.querySelectorAll(".aba-btn").forEach(btn => btn.classList.remove("ativa"));
  document.querySelectorAll(".aba-conteudo").forEach(sec => sec.classList.remove("ativa"));

  event.currentTarget.classList.add("ativa");
  const alvo = document.getElementById(`aba-${idAba}`);
  if (alvo) alvo.classList.add("ativa");

  if (idAba === "dsa-visual") {
    atualizarVisualizadorDSA();
  } else if (idAba === "metricas") {
    carregarEstatisticas();
  }
}

// ==============================================================================
// 1. CARREGAMENTO E CRUD DE SERVIÇOS
// ==============================================================================
async function carregarServicos() {
  try {
    const res = await fetch(`${API_BASE}/api/servicos`);
    const dados = await res.json();
    if (dados.sucesso) {
      servicosAtuais = dados.servicos;
      renderizarTabela(servicosAtuais);
      atualizarIndicadorTotal(dados.total);
    }
  } catch (err) {
    console.error("Erro ao carregar serviços:", err);
  }
}

function renderizarTabela(lista) {
  const corpo = document.getElementById("tabelaCorpo");
  const msgVazia = document.getElementById("mensagemSemRegistros");
  corpo.innerHTML = "";

  if (!lista || lista.length === 0) {
    msgVazia.classList.remove("oculto");
    return;
  }
  msgVazia.classList.add("oculto");

  lista.forEach(s => {
    const tr = document.createElement("tr");

    const classeTag = obterClasseCategoria(s.categoria);
    const classeStatus = obterClasseStatus(s.status);

    tr.innerHTML = `
      <td><strong>#${String(s.id).padStart(3, '0')}</strong></td>
      <td>
        <strong>${s.titulo}</strong>
        <div style="font-size: 0.78rem; color: #64748b;">${s.local_atendimento}</div>
      </td>
      <td><span class="badge-tag ${classeTag}">${s.categoria}</span></td>
      <td>${s.tempo_estimado_dias} dia(s)</td>
      <td><span class="${classeStatus}">● ${s.status}</span></td>
      <td style="text-align: center;">
        <button class="btn-acao btn-acao-detalhe" onclick="abrirDetalhes(${s.id})" title="Ver Detalhes">🔍 Ver</button>
        <button class="btn-acao btn-acao-editar" onclick="abrirEdicao(${s.id})" title="Editar">✏️ Editar</button>
        <button class="btn-acao btn-acao-excluir" onclick="solicitarExclusao(${s.id}, '${s.titulo.replace(/'/g, "\\'")}')" title="Excluir">🗑️</button>
      </td>
    `;
    corpo.appendChild(tr);
  });
}

function obterClasseCategoria(cat) {
  const map = {
    "Saúde": "tag-saude",
    "Assistência Social": "tag-assistencia",
    "Documentação e Cidadania": "tag-documentacao",
    "Educação e Qualificação": "tag-educacao",
    "Serviços Urbanos": "tag-urbanos"
  };
  return map[cat] || "tag-saude";
}

function obterClasseStatus(st) {
  if (st === "Ativo") return "status-ativo";
  if (st === "Em Atualização") return "status-atualizacao";
  return "status-suspenso";
}

function atualizarIndicadorTotal(total) {
  const el = document.getElementById("indicadorStatus");
  if (el) el.textContent = `🟢 Lista Encadeada: ${total} Nós`;
}

// ==============================================================================
// 2. BUSCA COM MÉTRICAS DE DSA
// ==============================================================================
async function executarBusca() {
  const termo = document.getElementById("campoBusca").value.trim();
  const campo = document.getElementById("filtroCampoBusca").value;

  if (!termo) {
    carregarServicos();
    fecharAlertaBusca();
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/busca?campo=${encodeURIComponent(campo)}&termo=${encodeURIComponent(termo)}`);
    const dados = await res.json();
    if (dados.sucesso) {
      renderizarTabela(dados.resultados);
      exibirAlertaBusca(dados.metricas);
    }
  } catch (err) {
    console.error("Erro na busca:", err);
  }
}

function aoDigitarBusca(event) {
  if (event.key === "Enter") {
    executarBusca();
  }
}

function limparBusca() {
  document.getElementById("campoBusca").value = "";
  fecharAlertaBusca();
  carregarServicos();
}

function exibirAlertaBusca(metricas) {
  const alerta = document.getElementById("alertaMetricasBusca");
  const titulo = document.getElementById("alertaBuscaTitulo");
  const texto = document.getElementById("alertaBuscaTexto");

  titulo.textContent = `${metricas.algoritmo}:`;
  texto.textContent = `${metricas.motivo} (Complexidade de nós inspecionados: ${metricas.comparacoes})`;
  alerta.classList.remove("oculto");
}

function fecharAlertaBusca() {
  const alerta = document.getElementById("alertaMetricasBusca");
  if (alerta) alerta.classList.add("oculto");
}

// ==============================================================================
// 3. VISUALIZADOR DA ESTRUTURA DE DADOS (NÓS & PONTEIROS)
// ==============================================================================
async function atualizarVisualizadorDSA() {
  try {
    const res = await fetch(`${API_BASE}/api/nos-dsa`);
    const dados = await res.json();
    if (!dados.sucesso) return;

    document.getElementById("lblEnderecoHead").textContent = dados.cabeca_endereco;
    document.getElementById("lblTotalNos").textContent = dados.total_nos;

    const grade = document.getElementById("gradeNos");
    grade.innerHTML = "";

    if (dados.nos.length === 0) {
      grade.innerHTML = `<div class="no-nulo">HEAD -> NULL (Lista Vazia)</div>`;
      return;
    }

    dados.nos.forEach((no, idx) => {
      const card = document.createElement("div");
      card.className = "card-no";

      const proxTexto = no.proximo_id !== null ? `Prox ID: #${no.proximo_id}` : `NULL (Fim)`;

      card.innerHTML = `
        <div class="no-topo">
          <span>NÓ #${String(no.indice).padStart(2, '0')}</span>
          <span>${no.endereco_memoria_no.slice(-6)}</span>
        </div>
        <div class="no-conteudo">
          <div class="no-titulo" title="${no.titulo}">ID ${no.id} - ${no.titulo}</div>
          <div class="no-cat">${no.categoria}</div>
        </div>
        <div class="no-ponteiro">
          ↳ .proximo: <strong>${proxTexto}</strong>
        </div>
      `;

      grade.appendChild(card);

      // Seta indicativa de encadeamento
      if (idx < dados.nos.length - 1) {
        const seta = document.createElement("div");
        seta.className = "seta-encadeamento";
        seta.textContent = "➔";
        grade.appendChild(seta);
      }
    });

    // Fim da lista aponta para NULL
    const setaFim = document.createElement("div");
    setaFim.className = "seta-encadeamento";
    setaFim.textContent = "➔";
    grade.appendChild(setaFim);

    const noNulo = document.createElement("div");
    noNulo.className = "no-nulo";
    noNulo.textContent = "NULL";
    grade.appendChild(noNulo);

  } catch (err) {
    console.error("Erro ao carregar visualização DSA:", err);
  }
}

// ==============================================================================
// 4. BANCADA DE ALGORITMOS (MERGE SORT / INSERTION SORT)
// ==============================================================================
async function executarOrdenacao(aplicarPrincipal) {
  const criterio = document.getElementById("selCriterio").value;
  const algoritmo = document.getElementById("selAlgoritmo").value;
  const ordem = document.getElementById("selOrdem").value;
  const asc = (ordem === "asc");

  try {
    const res = await fetch(`${API_BASE}/api/ordenar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        criterio: criterio,
        algoritmo: algoritmo,
        asc: asc,
        aplicar_principal: aplicarPrincipal
      })
    });

    const dados = await res.json();
    if (dados.sucesso) {
      exibirResultadoAlgoritmo(dados.metricas);
      renderizarPreviaOrdenada(dados.servicos);

      if (aplicarPrincipal) {
        alert("✅ Lista principal reordenada com sucesso na memória!");
        carregarServicos();
      }
    }
  } catch (err) {
    console.error("Erro na ordenação:", err);
  }
}

function exibirResultadoAlgoritmo(metricas) {
  document.getElementById("painelMetricas").classList.remove("oculto");
  document.getElementById("resAlgoNome").textContent = metricas.algoritmo;
  document.getElementById("resAlgoQtd").textContent = metricas.elementos_ordenados;
  document.getElementById("resAlgoComparacoes").textContent = metricas.comparacoes;
  document.getElementById("resAlgoReligacoes").textContent = metricas.religacoes_ponteiros;
  document.getElementById("resAlgoTempo").textContent = `${metricas.tempo_execucao_ms} ms`;
}

function renderizarPreviaOrdenada(servicos) {
  const container = document.getElementById("previaOrdenadaCorpo");
  container.innerHTML = "";

  servicos.forEach(s => {
    const item = document.createElement("div");
    item.className = "previa-item";
    item.innerHTML = `
      <span><strong>[ID ${String(s.id).padStart(3, '0')}]</strong> ${s.titulo}</span>
      <span class="badge-tag ${obterClasseCategoria(s.categoria)}">${s.categoria}</span>
      <span>Prazo: ${s.tempo_estimado_dias}d</span>
    `;
    container.appendChild(item);
  });
}

// ==============================================================================
// 5. ANÁLISE E ESTATÍSTICAS
// ==============================================================================
async function carregarEstatisticas() {
  try {
    const res = await fetch(`${API_BASE}/api/estatisticas`);
    const dados = await res.json();
    if (!dados.sucesso) return;

    const st = dados.estatisticas;
    document.getElementById("kpiTotalRegistros").textContent = st.total_registros;
    document.getElementById("kpiTempoMedio").textContent = `${st.tempo_medio_dias} d`;
    document.getElementById("kpiTotalCategorias").textContent = Object.keys(st.por_categoria).length;
    document.getElementById("kpiServicosAtivos").textContent = st.por_status["Ativo"] || 0;

    // Barras de Categorias
    const barrasContainer = document.getElementById("barrasCategorias");
    barrasContainer.innerHTML = "";

    for (const [cat, qtd] of Object.entries(st.por_categoria)) {
      const perc = st.distribuicao_percentual[cat] || 0;
      const div = document.createElement("div");
      div.className = "barra-linha";
      div.innerHTML = `
        <div class="barra-cabecalho">
          <span>${cat} (${qtd})</span>
          <span>${perc}%</span>
        </div>
        <div class="barra-trilho">
          <div class="barra-preenchimento" style="width: ${perc}%;"></div>
        </div>
      `;
      barrasContainer.appendChild(div);
    }

    // Barras de Status
    const statusContainer = document.getElementById("listaStatus");
    statusContainer.innerHTML = "";

    for (const [statusNome, qtd] of Object.entries(st.por_status)) {
      const perc = Math.round((qtd / st.total_registros) * 100);
      const div = document.createElement("div");
      div.className = "barra-linha";
      div.innerHTML = `
        <div class="barra-cabecalho">
          <span>${statusNome} (${qtd})</span>
          <span>${perc}%</span>
        </div>
        <div class="barra-trilho">
          <div class="barra-preenchimento" style="width: ${perc}%; background: ${statusNome === 'Ativo' ? '#16a34a' : '#d97706'};"></div>
        </div>
      `;
      statusContainer.appendChild(div);
    }

  } catch (err) {
    console.error("Erro ao carregar estatísticas:", err);
  }
}

// ==============================================================================
// 6. MODAIS E CADASTRO / EDIÇÃO
// ==============================================================================
function abrirModalCadastro() {
  document.getElementById("formModoEdicao").value = "0";
  document.getElementById("formTituloModal").textContent = "Cadastrar Novo Serviço Público";
  document.getElementById("btnSalvarForm").textContent = "Salvar Registro na Lista Encadeada";
  document.getElementById("formId").disabled = false;
  document.getElementById("formServico").reset();
  document.getElementById("modalFormulario").classList.remove("oculto");
}

async function abrirEdicao(id) {
  const servico = servicosAtuais.find(s => s.id === id);
  if (!servico) return;

  document.getElementById("formModoEdicao").value = "1";
  document.getElementById("formTituloModal").textContent = `Editar Serviço [ID ${servico.id}]`;
  document.getElementById("btnSalvarForm").textContent = "Salvar Alterações";
  document.getElementById("formId").value = servico.id;
  document.getElementById("formId").disabled = true;

  document.getElementById("formTitulo").value = servico.titulo;
  document.getElementById("formCategoria").value = servico.categoria;
  document.getElementById("formTempo").value = servico.tempo_estimado_dias;
  document.getElementById("formStatus").value = servico.status;
  document.getElementById("formDescricao").value = servico.descricao;
  document.getElementById("formRequisitos").value = servico.requisitos;
  document.getElementById("formLocal").value = servico.local_atendimento;
  document.getElementById("formPublico").value = servico.publico_alvo;

  document.getElementById("modalFormulario").classList.remove("oculto");
}

function fecharModalFormulario() {
  document.getElementById("modalFormulario").classList.add("oculto");
}

async function salvarFormulario(event) {
  event.preventDefault();
  const modoEdicao = document.getElementById("formModoEdicao").value === "1";
  const id = parseInt(document.getElementById("formId").value);

  const payload = {
    id: id,
    titulo: document.getElementById("formTitulo").value.trim(),
    categoria: document.getElementById("formCategoria").value,
    tempo_estimado_dias: parseInt(document.getElementById("formTempo").value),
    status: document.getElementById("formStatus").value,
    descricao: document.getElementById("formDescricao").value.trim(),
    requisitos: document.getElementById("formRequisitos").value.trim(),
    local_atendimento: document.getElementById("formLocal").value.trim(),
    publico_alvo: document.getElementById("formPublico").value.trim()
  };

  try {
    let url = `${API_BASE}/api/servicos`;
    let metodo = "POST";

    if (modoEdicao) {
      url = `${API_BASE}/api/servicos/${id}`;
      metodo = "PUT";
    }

    const res = await fetch(url, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const resposta = await res.json();
    if (!res.ok || !resposta.sucesso) {
      alert(`Erro: ${resposta.mensagem}`);
      return;
    }

    alert(resposta.mensagem || "Operação realizada com sucesso!");
    fecharModalFormulario();
    carregarServicos();
    carregarEstatisticas();
  } catch (err) {
    alert("Erro na conexão com o servidor.");
    console.error(err);
  }
}

async function abrirDetalhes(id) {
  const servico = servicosAtuais.find(s => s.id === id);
  if (!servico) return;

  document.getElementById("detalheTituloModal").textContent = `[ID ${servico.id}] ${servico.titulo}`;
  const corpo = document.getElementById("detalheCorpoConteudo");
  corpo.innerHTML = `
    <div class="detalhe-item"><strong>Categoria:</strong> <span class="badge-tag ${obterClasseCategoria(servico.categoria)}">${servico.categoria}</span></div>
    <div class="detalhe-item"><strong>Status:</strong> <span class="${obterClasseStatus(servico.status)}">● ${servico.status}</span></div>
    <div class="detalhe-item"><strong>Prazo de Atendimento:</strong> ${servico.tempo_estimado_dias} dia(s) úteis</div>
    <div class="detalhe-item"><strong>Local / Canal:</strong> ${servico.local_atendimento}</div>
    <div class="detalhe-item"><strong>Público-Alvo:</strong> ${servico.publico_alvo}</div>
    <div class="detalhe-item" style="margin-top: 15px;">
      <strong>Descrição do Serviço:</strong>
      <p style="margin-top: 4px; color: #475569;">${servico.descricao}</p>
    </div>
    <div class="detalhe-item" style="margin-top: 15px;">
      <strong>Requisitos e Documentação:</strong>
      <p style="margin-top: 4px; color: #475569;">${servico.requisitos}</p>
    </div>
  `;

  document.getElementById("modalDetalhes").classList.remove("oculto");
}

function fecharModalDetalhes() {
  document.getElementById("modalDetalhes").classList.add("oculto");
}

async function solicitarExclusao(id, titulo) {
  const confirma = confirm(`Tem certeza que deseja excluir o serviço abaixo da Lista Encadeada?\n\n[ID ${id}] ${titulo}\n\nOs nós e referências serão reorganizados.`);
  if (!confirma) return;

  try {
    const res = await fetch(`${API_BASE}/api/servicos/${id}`, { method: "DELETE" });
    const dados = await res.json();
    if (dados.sucesso) {
      alert(dados.mensagem);
      carregarServicos();
      carregarEstatisticas();
    } else {
      alert(`Falha: ${dados.mensagem}`);
    }
  } catch (err) {
    console.error("Erro na exclusão:", err);
    alert("Falha ao se comunicar com o servidor.");
  }
}

function abrirModalSobre() {
  document.getElementById("modalSobre").classList.remove("oculto");
}

function fecharModalSobre() {
  document.getElementById("modalSobre").classList.add("oculto");
}

