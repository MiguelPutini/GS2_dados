# DOCUMENTAÇÃO TÉCNICA DO PROJETO

**Global Solution 2026.2 — Citizen Tech**  
**Citizen Assist AI | Data Structures and Algorithms (DSA)**  
**Linguagem:** Python 3.12  
**Repositório:** https://github.com/MiguelPutini/GS2_dados.git  

### 👥 Integrantes da Equipe
- **Miguel Putini** — RM 571624
- **Alexandre Rizzi** — RM 569621
- **Lucas Klein de Veiga** — RM 570029

---

## 1. Descrição do Recorte Escolhido

O projeto **Citizen Assist AI** tem como missão central organizar, estruturar e disponibilizar informações cruciais sobre serviços públicos, direitos do cidadão, documentação civil e orientações cotidianas. 

Em conformidade com as diretrizes do edital da Global Solution 2026.2, o recorte temático adotado abrange **cinco eixos essenciais da administração pública**, estruturados para atender diretamente às necessidades cotidianas do cidadão:

1. **Saúde:** Marcação de consultas eletivas em Unidades Básicas de Saúde (UBS), calendário e campanhas de vacinação (PNI) e dispensação de medicamentos especializados de alto custo (DME).
2. **Assistência Social:** Inscrição e atualização no Cadastro Único (CadÚnico), acesso a benefícios de transferência de renda e atendimento emergencial a famílias em vulnerabilidade no CRAS/CREAS.
3. **Documentação e Cidadania:** Emissão da nova Carteira de Identidade Nacional (CIN), certidão de quitação eleitoral, emissão e regularização de documentos civis básicos.
4. **Educação e Qualificação:** Vagas para a Educação de Jovens e Adultos (EJA), inscrição em cursos gratuitos de formação e qualificação tecnológica voltados à empregabilidade.
5. **Serviços Urbanos:** Solicitações de zeladoria urbana, manutenção e reparo de iluminação pública, operação tapa-buracos e avaliação para poda de árvores em vias públicas.

---

## 2. Modelo dos Registros (`ServicoPublico`)

Cada serviço ou orientação ao cidadão é modelado como uma entidade rica, encapsulada na classe `ServicoPublico` (`src/modelos/servico.py`). 

A entidade não apenas transporta dados, mas aplica **validações ativas** de integridade em tempo de instanciação:

| Atributo | Tipo | Descrição | Regras de Validação |
|---|---|---|---|
| `id` | `int` | Identificador único positivo do serviço público | Obrigatório; deve ser número inteiro maior que zero (`id > 0`). Rejeita tipos incompatíveis e IDs nulos ou negativos. |
| `titulo` | `str` | Denominação formal do serviço ou orientação pública | Obrigatório; não pode ser string vazia ou contendo apenas espaços em branco. |
| `categoria` | `str` | Eixo temático do serviço público | Pertencente ao domínio: *Saúde*, *Assistência Social*, *Documentação e Cidadania*, *Educação e Qualificação*, *Serviços Urbanos*. |
| `descricao` | `str` | Detalhamento sobre a finalidade e funcionamento do serviço | Obrigatório; texto informativo sem conteúdo nulo. |
| `requisitos` | `str` | Documentos exigidos, laudos e critérios de elegibilidade | Obrigatório; orienta previamente o cidadão antes do deslocamento. |
| `local_atendimento` | `str` | Unidade física (UBS, CRAS, Poupatempo) ou canal digital | Obrigatório; identifica onde obter o atendimento. |
| `publico_alvo` | `str` | Cidadãos aos quais o serviço é destinado | Ex: *Munícipes em geral*, *População de baixa renda*, *Jovens e adultos*. |
| `tempo_estimado_dias` | `int` | Prazo médio de conclusão do atendimento (dias úteis) | Inteiro não negativo (`>= 0`). 0 indica atendimento imediato. |
| `status` | `str` | Situação de disponibilidade do serviço | *Ativo*, *Em Atualização* ou *Suspenso*. |

---

## 3. Estrutura de Dados: Lista Simplesmente Encadeada

Conforme exigência do edital (*"Os dados deverão ser mantidos em uma lista encadeada implementada pela equipe... representar os nós com classes, objetos e referências"*), o sistema **não** utiliza arrays ou coleções nativas como estrutura principal de armazenamento de nós.

### 3.1. Classe `Node` (`src/estruturas/no.py`)

A classe `Node` modela cada elo da corrente de dados em memória:
- **`dado`**: referência para a instância do registro `ServicoPublico`.
- **`proximo`**: referência/ponteiro (`Optional[Node]`) para o próximo nó da lista encadeada, ou `None` caso seja o último nó (cauda).

```text
  [Nó 1]                     [Nó 2]                     [Nó 3]
+--------------------+     +--------------------+     +--------------------+
| dado: Servico #105 |     | dado: Servico #101 |     | dado: Servico #109 |
| proximo: ----------+---->| proximo: ----------+---->| proximo: None      |
+--------------------+     +--------------------+     +--------------------+
```

### 3.2. Classe `ListaEncadeada` (`src/estruturas/lista_encadeada.py`)

Gerencia o encadeamento a partir do ponteiro de entrada `cabeca` (Head) e mantém o controle de cardinalidade em `_tamanho`.

Principais operações implementadas:
- `inserir_inicio(servico)`: Aloca novo nó apontando para a cabeça atual e redefine `self.cabeca`. Operação $O(1)$.
- `inserir_fim(servico)`: Percorre até o último nó cujo ponteiro `proximo` é `None` e conecta o novo nó. Operação $O(n)$.
- `remover_por_id(id_servico)`: Localiza o nó alvo e ajusta os ponteiros entre o antecessor e o sucessor (`anterior.proximo = atual.proximo`), isolando o nó removido e preservando a integridade da lista.
- `buscar_por_id(id_servico)`: Percorre sequencialmente nó a nó avaliando `atual.dado.id == id_servico`.
- `existe_id(id_servico)`: Impede a inserção de chaves primárias duplicadas na lista.
- `percurso()` e `__iter__()`: Permite caminhar pela lista sequencialmente sem violar o encapsulamento.
- `inspecionar_ponteiros()`: Extrai os endereços em memória física (`hex(id(no))`) e as referências `.proximo` para inspeção do professor e apresentação gráfica.
- `gerar_estatisticas()`: Processa em um único percurso as agregações por categoria, status e tempo médio.

---

## 4. Funcionamento do Menu Interativo (CLI)

O menu interativo via terminal (`src/cli/menu.py`) foi estruturado para fornecer uma experiência robusta e amigável:

```text
====================================================================
*   GLOBAL SOLUTION 2026.2 | CITIZEN TECH - CITIZEN ASSIST AI    *
*   Gerenciamento de Serviços Públicos com Estruturas de Dados   *
====================================================================
Status da Lista Encadeada: 12 registro(s) armazenado(s)
--------------------------------------------------------------------
[1]  Cadastrar Novo Serviço Público (com ID único)
[2]  Consultar Serviço por Identificador (Busca por ID)
[3]  Pesquisar Serviços por Atributo (Título, Categoria, Geral)
[4]  Listar Todos os Serviços (Percurso da Lista Encadeada)
[5]  Atualizar Serviço Existente
[6]  Excluir Serviço (Remoção e religação de nós)
[7]  Ordenar Registros (Merge Sort / Insertion Sort / Selection Sort)
[8]  Apresentar Análise e Estatísticas (Processamento dos Dados)
[9]  Inspecionar Topologia de Nós e Ponteiros (Evidência DSA)
[10] Carregar Dados Iniciais de Demonstração (Seed)
[11] Salvar Alterações em Arquivo
[0]  Encerrar o Sistema
--------------------------------------------------------------------
```

### Tratamento de Falhas e Validação de Entradas:
1. **Entradas Não Numéricas:** Função `ler_inteiro` intercepta exceções do tipo `ValueError`, repassando aviso orientativo e solicitando nova digitação sem abortar o programa.
2. **Opções Inexistentes no Menu:** Validação contínua do intervalo $[0, 11]$.
3. **Strings Vazias:** Função `ler_texto(obrigatorio=True)` impede submissão de campos em branco.
4. **Identificadores Duplicados:** Checagem imediata via `lista.existe_id(id)`. Se o ID já existir, o cadastro é abortado e o usuário é notificado.
5. **Consultas Sem Resultado:** O sistema exibe relatório claro informando quantas comparações foram executadas e notificando amigavelmente a ausência de registros.
6. **Operações em Lista Vazia:** Todas as operações (consulta, atualização, exclusão, ordenação, relatórios) possuem salvaguardas que impedem erros de desreferenciação nula (`AttributeError: 'NoneType' object has no attribute '...'`).

---

## 5. Arquitetura Modular do Código

O projeto adota separação clara de responsabilidades:

```text
c:\Users\migue\Desktop\gs_dados\
├── src/
│   ├── modelos/           # Classes de domínio e validação (ServicoPublico)
│   ├── estruturas/        # Implementação pura de DSA (Node, ListaEncadeada)
│   ├── algoritmos/        # Algoritmos manuais de Busca e Ordenação
│   ├── persistencia/      # Carga JSON e persistência dos dados
│   ├── cli/               # Menu interativo em terminal
│   └── web/               # Servidor HTTP RESTful e Frontend (Opcional rico)
├── dados/                 # Base JSON de demonstração
├── testes/                # Suíte completa de testes automatizados (unittest)
├── main.py                # Executável CLI principal
├── web_app.py             # Executável do Portal Web
├── demo.py                # Script de demonstração guiada
└── scripts .bat           # Execução com 1 clique no Windows
```

