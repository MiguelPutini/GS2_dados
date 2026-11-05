# ANÁLISE DE COMPLEXIDADE ALGORÍTMICA (BIG-O)

**Global Solution 2026.2 — Citizen Tech**  
**Citizen Assist AI | Data Structures and Algorithms (DSA)**  

### 👥 Integrantes da Equipe
- **Miguel Putini** — RM 571624
- **Alexandre Rizzi** — RM 569621
- **Lucas Klein de Veiga** — RM 570029

---

## 1. Quadro Resumo de Complexidade Assintótica

A tabela a seguir consolida a análise de complexidade temporal e espacial de todas as operações e algoritmos implementados no **Citizen Assist AI**:

| Operação / Algoritmo | Melhor Caso ($\Omega$) | Caso Médio ($\Theta$) | Pior Caso ($O$) | Complexidade Espacial Auxiliar | Justificativa Sintética |
|---|---|---|---|---|---|
| **Inserção na Cabeça** (`inserir_inicio`) | $\Omega(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ | Ajuste direto de ponteiros na entrada da lista. |
| **Inserção no Fim** (`inserir_fim`) | $\Omega(n)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ | Percurso sequencial da cabeça até o nó cujo `proximo` é `None`. |
| **Remoção por ID** (`remover_por_id`) | $\Omega(1)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ | $\Omega(1)$ se for a cabeça; $O(n)$ se estiver no meio, fim ou ausente. |
| **Busca Linear por ID** (`busca_linear_id`) | $\Omega(1)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ | $\Omega(1)$ se o alvo for o primeiro nó; $O(n)$ se for o último ou inexistente. |
| **Busca por Atributo** (`busca_linear_atributo`)| $\Omega(n)$ | $\Theta(n)$ | $O(n)$ | $O(k)$ | Varre todos os nós para identificar todas as correspondências parciais. |
| **Busca Binária** (`busca_binaria_em_vetor`) | $\Omega(1)$ | $\Theta(\log n)$ | $O(\log n)$ | $O(1)$ | Divisão sucessiva do espaço de busca em coleção ordenada indexável. |
| **Merge Sort em Lista Encadeada** | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $O(n \log n)$ | $O(\log n)$ | Divisão ao meio por ponteiros lento/rápido e intercalação de nós. |
| **Insertion Sort em Lista Encadeada** | $\Omega(n)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ | $\Omega(n)$ se já ordenada; $O(n^2)$ se invertida ou aleatória. |
| **Selection Sort** | $\Omega(n^2)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ | Compara todos os pares para identificar o mínimo em cada iteração. |
| **Geração de Estatísticas** (`gerar_estatisticas`) | $\Omega(n)$ | $\Theta(n)$ | $O(n)$ | $O(C)$ | Percurso único dos $n$ nós agregando em tabela de $C$ categorias. |

---

## 2. Análise Detalhada das Operações da Lista Encadeada

### 2.1. Inserção (`inserir_inicio` vs `inserir_fim`)
- **Inserção no Início:**
  - **Procedimento:** Cria-se o novo nó `novo_no = Node(dado, proximo=self.cabeca)` e redefine-se `self.cabeca = novo_no`.
  - **Complexidade:** $O(1)$ temporal e espacial. Não há qualquer laço de repetição ou dependência do volume $n$ de registros já armazenados.
- **Inserção no Fim:**
  - **Procedimento:** Como a lista simplesmente encadeada mantém apenas o ponteiro da cabeça, para adicionar um elemento ao fim é obrigatório percorrer os $n$ nós até encontrar `atual.proximo is None`.
  - **Complexidade:** $O(n)$ temporal. Caso mantivéssemos um ponteiro direto para a cauda (`tail`), a inserção no fim se tornaria $O(1)$, porém aumentaria a complexidade de manutenção nas remoções.

### 2.2. Remoção por Identificador (`remover_por_id`)
- **Procedimento:**
  1. Verifica se a lista está vazia ($O(1)$).
  2. Verifica se o elemento a remover é a própria cabeça ($O(1)$): se for, faz `self.cabeca = self.cabeca.proximo`.
  3. Caso contrário, utiliza dois ponteiros (`anterior` e `atual`) para caminhar pela lista até encontrar o nó desejado. Ao encontrar, conecta `anterior.proximo = atual.proximo`, desconectando o nó alvo.
- **Casos:**
  - **Melhor Caso $\Omega(1)$:** O elemento a ser removido é o primeiro nó (cabeça).
  - **Pior Caso $O(n)$:** O elemento está no último nó ou não existe na lista encadeada (sendo necessário percorrer todos os $n$ elementos para constatar sua ausência).
  - **Caso Médio $\Theta(n)$:** Em média, examinam-se $n / 2$ elementos.
  - **Memória:** $O(1)$ pois reutiliza os nós existentes sem alocação adicional.

---

## 3. Análise Detalhada dos Algoritmos de Busca

### 3.1. Busca Linear por Identificador (`busca_linear_id`)
- **Funcionamento:** Inicia no nó apontado por `self.cabeca` e avança via `atual = atual.proximo`, incrementando o contador de comparações e testando `atual.dado.id == id_procurado`.
- **Comportamento quando o registro não é encontrado:** O laço finaliza quando `atual is None`. O método retorna `(None, metricas)`, documentando explicitamente que todos os $n$ nós foram inspecionados sem sucesso, sem propagar exceções e permitindo tratamento amigável na interface.
- **Complexidade:**
  - **Melhor Caso $\Omega(1)$:** O elemento buscado reside no primeiro nó da lista (1 comparação).
  - **Pior Caso $O(n)$:** O elemento é o último ou não está presente na lista ($n$ comparações).
  - **Espaço:** $O(1)$ de memória auxiliar.

### 3.2. Busca Linear por Atributo (`busca_linear_atributo`)
- **Funcionamento:** Realiza busca de substring (*case-insensitive*) nos campos de título, categoria ou busca global.
- **Complexidade:**
  - **Temporal:** Obrigatoriamente $O(n)$ em todos os casos (Melhor, Médio e Pior), pois mesmo que encontre um registro correspondente na primeira posição, a lista pode conter outros registros na mesma categoria ou com o mesmo termo no título. Logo, a varredura completa de todos os $n$ nós é indispensável.
  - **Espacial:** $O(k)$, onde $k \le n$ é a quantidade de serviços que atenderam ao critério de busca.

### 3.3. Análise Comparativa: Busca Linear na Lista vs. Busca Binária
A Busca Binária requer tempo $O(\log n)$ por efetuar divisões consecutivas do espaço de busca. No entanto, em termos fundamentais de Estruturas de Dados:
- A Busca Binária clássica pressupõe **acesso aleatório indexado $O(1)$** aos elementos intermediários (como em arrays e vetores).
- Em uma lista simplesmente encadeada, acessar o elemento central demanda percurso sequencial de $n / 2$ nós ($O(n)$), o que anula a vantagem da busca binária direta sobre listas encadeadas sem o uso de estruturas auxiliares como *Skip Lists*.
- No projeto, demonstrou-se formalmente a Busca Binária em vetor ordenado (`busca_binaria_em_vetor`) para evidenciar aos avaliadores o contraste teórico e prático entre os paradigmas de acesso contíguo vs. encadeado.

---

## 4. Análise Detalhada dos Algoritmos de Ordenação

O edital estabelece explicitamente: *"Implementar pelo menos um algoritmo de ordenação estudado (Selection Sort, Insertion Sort, Merge Sort ou Quick Sort). O uso exclusivo de funções prontas de ordenação não atende ao requisito."*

Nossa solução implementou do zero **Merge Sort**, **Insertion Sort** e **Selection Sort** adaptados especificamente para a estrutura de Lista Encadeada.

### 4.1. Merge Sort em Lista Encadeada (Algoritmo Recomendado)

O **Merge Sort** é universalmente reconhecido como o algoritmo ideal para listas encadeadas devido à sua estratégia de *Divisão e Conquista* e à facilidade de intercalar nós sem necessidade de arrays intermediários.

#### Estrutura do Algoritmo:
1. **Divisão (Técnica dos Ponteiros Lento e Rápido):**
   Utiliza a técnica *Slow & Fast Pointer* (Lebre e Tartaruga de Floyd):
   - O ponteiro `rapido` avança dois nós por passo (`rapido.proximo.proximo`).
   - O ponteiro `lento` avança um nó por passo (`lento.proximo`).
   - Quando `rapido` atinge o final, `lento` está exatamente no ponto médio da lista.
   - A lista é dividida em duas desconectando `lento.proximo = None`. Tempo da divisão: $O(n)$.
2. **Conquista (Recursão):**
   Chama recursivamente o algoritmo para a metade esquerda e metade direita até chegar a listas de 0 ou 1 nó (caso base). A profundidade da árvore recursiva é $\log_2 n$.
3. **Intercalação (`_intercalar`):**
   Compara os nós da cabeça das duas listas parciais e religa as referências `.proximo` usando um nó sentinela (*dummy node*). Tempo da intercalação: $O(n)$.

#### Análise Formal de Complexidade:
- **Relação de Recorrência:**
  $$T(n) = 2T(n/2) + O(n)$$
  Pelo Teorema Mestre (Caso 2), temos que:
  $$T(n) = \Theta(n \log n)$$
- **Melhor Caso:** $\Omega(n \log n)$
- **Caso Médio:** $\Theta(n \log n)$
- **Pior Caso:** $O(n \log n)$
- **Estabilidade:** Sim, preserva a ordem relativa de registros com chaves iguais.
- **Espaço Auxiliar:** $O(\log n)$ exclusivamente devido à pilha de chamadas da recursão. Nenhuma cópia de arrays é necessária: os nós originais são religados diretamente através dos seus ponteiros.

### 4.2. Insertion Sort em Lista Encadeada

O **Insertion Sort** constrói a lista ordenada mantendo uma sublista inicialmente vazia e inserindo cada nó da lista original em sua posição correta na sublista.

#### Análise Formal:
- **Melhor Caso $\Omega(n)$:** Ocorre se a lista já estiver previamente ordenada no critério desejado. Cada nó precisa ser comparado apenas uma vez com a cauda da sublista ordenada ($n - 1$ comparações).
- **Pior Caso $O(n^2)$:** Ocorre quando a lista está na ordem exatamente inversa. Para inserir o $i$-ésimo nó, são necessárias $i$ comparações e percursos:
  $$\sum_{i=1}^{n-1} i = \frac{n(n-1)}{2} = \Theta(n^2)$$
- **Caso Médio $\Theta(n^2)$:** Em média, percorrem-se metade dos nós já ordenados a cada inserção.
- **Espaço Auxiliar:** $O(1)$ — algoritmo *in-place*.

### 4.3. Comparativo Experimental (Base de Teste: 12 Serviços Reais)

Executando a ordenação dos 12 registros de exemplo da base inicial por ID:

| Métrica | Merge Sort | Insertion Sort | Vantagem Prática |
|---|---|---|---|
| **Comparações de Chaves** | 32 comparações | 57 comparações | Merge Sort realizou **43,8% menos comparações**. |
| **Religações de Ponteiros**| 43 religações | 12 religações | Insertion Sort realizou menos ajustes de ponteiros locais. |
| **Tempo de Execução** | ~0.029 ms | ~0.018 ms | Em $n$ muito pequeno, o overhead da recursão torna Insertion Sort competitivo; para $n > 50$, Merge Sort domina assintoticamente. |

---

## 5. Análise do Processamento Analítico (`gerar_estatisticas`)

O requisito 3.5 do edital exige a produção de informações agregadas úteis (como quantidade de serviços por categoria, total de registros ou distribuição percentual).

- **Algoritmo:** Em um único percurso da cabeça até o nó nulo da lista encadeada, alimentam-se dicionários hash com as contagens de categorias e status, acumulando também a soma dos prazos estimados.
- **Complexidade Temporal:** $O(n)$, pois cada nó é visitado exatamente uma vez.
- **Complexidade Espacial:** $O(C + S)$, onde $C$ é o número de categorias distintas (máximo de 5) e $S$ o número de status (máximo de 3). Sendo constantes com relação a $n$, o espaço auxiliar é $O(1)$.

