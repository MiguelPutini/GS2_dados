# RELATÓRIO DE EVIDÊNCIAS DE TESTES

**Global Solution 2026.2 — Citizen Tech**  
**Citizen Assist AI | Data Structures and Algorithms (DSA)**  
**Status da Suíte de Testes:** 100% APROVADO (18 de 18 testes unitários e de integração)  

### 👥 Integrantes da Equipe
- **Miguel Putini** — RM 571624
- **Alexandre Rizzi** — RM 569621
- **Lucas Klein de Veiga** — RM 570029

---

## 1. Matriz Formal de Casos de Teste

A tabela a seguir documenta os cenários formais executados, cobrindo casos normais, registros inexistentes, entradas inválidas e operações de borda com lista vazia, conforme explicitamente exigido na Seção 4 e 6 do edital.

| ID | Categoria do Teste | Descrição do Cenário | Entrada de Dados | Resultado Esperado | Resultado Observado | Status |
|---|---|---|---|---|---|---|
| **TC-01** | *Caso Normal* | Cadastro válido de serviço público | ID=101, Título="Agendamento UBS", Cat="Saúde", Tempo=3d | Registro inserido na lista encadeada; tamanho incrementado | Inserido com sucesso; nó alocado na cauda; tamanho=1 | **PASSOU** |
| **TC-02** | *Caso Normal* | Percurso e encadeamento sequencial | Inserir IDs 10, 20 e 30 | Sequência de nós `10 -> 20 -> 30 -> NULL` | Cabeça aponta para 10; nó 10 aponta para 20; 20 para 30; 30 para None | **PASSOU** |
| **TC-03** | *Entrada Inválida* | Tentativa de cadastro com ID negativo | ID=-5, Título="Serviço X" | Lançamento de `ValueError` com mensagem orientativa | Exceção `ValueError: O identificador (ID) deve ser positivo` capturada | **PASSOU** |
| **TC-04** | *Entrada Inválida* | Tentativa de cadastro com ID textual | ID="ABC", Título="Serviço Y" | Lançamento de `ValueError` por tipo numérico inválido | Exceção `ValueError: ID inválido: ABC` capturada | **PASSOU** |
| **TC-05** | *Entrada Inválida* | Título em branco ou apenas espaços | ID=150, Título="   " | Rejeição por violação de campo obrigatório | Exceção `ValueError: O campo 'Título' é obrigatório` lançada | **PASSOU** |
| **TC-06** | *Caso de Borda* | Tentativa de cadastrar ID duplicado | ID=105 já existente na lista encadeada | Rejeição imediata antes da alocação de nó para preservar chave primária | `ValueError: Conflito de chave única: já existe um serviço com o ID 105` | **PASSOU** |
| **TC-07** | *Caso Normal* | Busca Linear por ID existente | ID procurado = 104 | Encontrar o registro de medicamento e retornar métricas de comparações | Objeto retornado com sucesso; 6 comparações realizadas | **PASSOU** |
| **TC-08** | *Registro Inexistente* | Busca Linear por ID inexistente | ID procurado = 9999 | Retornar `None` com log amigável e contador de comparações igual a $n$ | `None` retornado; total de comparações igual a 12 nós (pior caso) | **PASSOU** |
| **TC-09** | *Caso Normal* | Pesquisa por Atributo (Categoria) | Campo="categoria", Termo="Saúde" | Retornar todos os serviços daquela categoria (3 itens) | 3 registros retornados; tempo de busca $O(n)$ | **PASSOU** |
| **TC-10** | *Registro Inexistente* | Pesquisa por Atributo sem correspondência | Campo="titulo", Termo="TermoInexistenteXYZ" | Retornar lista vazia com mensagem de busca sem resultados | Lista vazia retornada; feedback de 0 registros encontrados | **PASSOU** |
| **TC-11** | *Caso Normal* | Atualização de campos de serviço | ID=950, Novo Título="Título Atualizado" | Campos modificados preservando o mesmo identificador | Dados alterados com sucesso; integridade da lista preservada | **PASSOU** |
| **TC-12** | *Caso Normal* | Remoção de nó no meio da lista | ID=20 em lista `[10 -> 20 -> 30]` | Desvinculação do nó 20; ponteiro do nó 10 religado para o nó 30 | Nó 20 desconectado; lista resultante `[10 -> 30]`; integridade preservada | **PASSOU** |
| **TC-13** | *Caso Normal* | Remoção de nó na cabeça da lista | ID=10 em lista `[10 -> 30]` | `self.cabeca` passa a apontar diretamente para o nó 30 | Cabeça redefinida com sucesso; nó 10 isolado; tamanho decrementado | **PASSOU** |
| **TC-14** | *Lista Vazia* | Remoção em lista vazia | `remover_por_id(999)` em lista com tamanho 0 | Retornar `None` de forma segura sem lançar exceção de ponteiro nulo | Retornou `None`; nenhuma quebra de execução | **PASSOU** |
| **TC-15** | *Lista Vazia* | Busca em lista vazia | `buscar_por_id(101)` em lista vazia | Retornar `None` sem falha | Retornou `None` com 0 comparações | **PASSOU** |
| **TC-16** | *Lista Vazia* | Ordenação de lista vazia | Executar Merge Sort e Insertion Sort em lista vazia | Retornar nova lista encadeada vazia sem erro | Listas vazias retornadas com 0 comparações registradas | **PASSOU** |
| **TC-17** | *Caso Normal* | Merge Sort por ID crescente | Lista com 12 registros fora de ordem | Lista ordenada em ordem estritamente crescente de ID | Sequência $[101, 102, 104, 105, ..., 116]$; 32 comparações | **PASSOU** |
| **TC-18** | *Caso Normal* | Merge Sort por Título (A-Z) | Critério="titulo", Ordem="asc" | Registros ordenados alfabeticamente pelos títulos | Lista reordenada com sucesso; nós reconectados | **PASSOU** |

---

## 2. Evidência Real da Execução Automatizada (`unittest`)

Comando executado:
```powershell
python -m unittest discover -s testes -v
```

Log oficial de execução e aprovação:
```text
test_busca_binaria_vetor_ordenado (test_sistema.TestAlgoritmosBusca.test_busca_binaria_vetor_ordenado) ... ok
test_busca_linear_atributo_titulo_e_categoria (test_sistema.TestAlgoritmosBusca.test_busca_linear_atributo_titulo_e_categoria) ... ok
test_busca_linear_id_existente (test_sistema.TestAlgoritmosBusca.test_busca_linear_id_existente) ... ok
test_busca_linear_id_inexistente (test_sistema.TestAlgoritmosBusca.test_busca_linear_id_inexistente) ... ok
test_insertion_sort_por_id (test_sistema.TestAlgoritmosOrdenacao.test_insertion_sort_por_id) ... ok
test_merge_sort_por_id_crescente (test_sistema.TestAlgoritmosOrdenacao.test_merge_sort_por_id_crescente) ... ok
test_merge_sort_por_id_decrescente (test_sistema.TestAlgoritmosOrdenacao.test_merge_sort_por_id_decrescente) ... ok
test_merge_sort_por_titulo (test_sistema.TestAlgoritmosOrdenacao.test_merge_sort_por_titulo) ... ok
test_ordenacao_lista_vazia (test_sistema.TestAlgoritmosOrdenacao.test_ordenacao_lista_vazia) ... ok
test_selection_sort_por_prazo (test_sistema.TestAlgoritmosOrdenacao.test_selection_sort_por_prazo) ... ok
test_insercao_inicio_e_fim (test_sistema.TestListaEncadeada.test_insercao_inicio_e_fim) ... ok
test_lista_inicialmente_vazia (test_sistema.TestListaEncadeada.test_lista_inicialmente_vazia) ... ok
test_operacoes_em_lista_vazia (test_sistema.TestListaEncadeada.test_operacoes_em_lista_vazia) ... ok
test_rejeicao_id_duplicado (test_sistema.TestListaEncadeada.test_rejeicao_id_duplicado) ... ok
test_remocao_cabeca_meio_fim (test_sistema.TestListaEncadeada.test_remocao_cabeca_meio_fim) ... ok
test_campos_obrigatorios_vazios (test_sistema.TestServicoPublico.test_campos_obrigatorios_vazios) ... ok
test_criacao_valida (test_sistema.TestServicoPublico.test_criacao_valida) ... ok
test_id_invalido_rejeicao (test_sistema.TestServicoPublico.test_id_invalido_rejeicao) ... ok

----------------------------------------------------------------------
Ran 18 tests in 0.001s

OK
```

---

## 3. Evidência das Proteções de Integridade em Tempo de Execução

### 3.1. Rejeição de ID Duplicado
```text
Tentando inserir um novo serviço com ID repetido (105)...
[SUCESSO NO BLOQUEIO]: Conflito de chave única: já existe um serviço cadastrado com o ID 105.
```

### 3.2. Busca por Registro Inexistente
```text
Executando busca por ID inexistente (ID 9999)...
-> Resultado: Nenhum registro com ID 9999 foi localizado na lista (total de comparações: 12).
   Total de nós examinados: 12 (pior caso O(n))
```

### 3.3. Comportamento com Lista Vazia
```text
Lista criada. Estado inicial: vazia=True | tamanho=0
Ponteiro da cabeça (self.cabeca): None
Executando remover_por_id(999) em lista vazia -> Retorno: None (seguro e sem erro de ponteiro).
```

