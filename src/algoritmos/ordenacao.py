"""
Implementações próprias de algoritmos de ordenação para Lista Encadeada.
NENHUMA função nativa de ordenação (como .sort() ou sorted()) é utilizada.
Atende integralmente aos requisitos de DSA da Global Solution.
"""

import time
from typing import Optional, Tuple, Dict, Any, Callable
from src.estruturas.no import Node
from src.estruturas.lista_encadeada import ListaEncadeada
from src.modelos.servico import ServicoPublico


def _obter_chave(servico: ServicoPublico, criterio: str):
    """Extrai o valor do campo escolhido para critério de ordenação."""
    criterio_limpo = criterio.lower().strip()
    if criterio_limpo == "id":
        return servico.id
    elif criterio_limpo in ("titulo", "título"):
        return servico.titulo.lower()
    elif criterio_limpo == "categoria":
        return servico.categoria.lower()
    elif criterio_limpo in ("prazo", "tempo", "tempo_estimado_dias"):
        return servico.tempo_estimado_dias
    elif criterio_limpo == "status":
        return servico.status.lower()
    return servico.id


def _comparar(servico_a: ServicoPublico, servico_b: ServicoPublico, criterio: str, asc: bool = True) -> int:
    """
    Função de comparação personalizada entre dois serviços.
    Retorna:
      -1 se A < B
       0 se A == B
       1 se A > B
    Inverte os sinais se asc=False (decrescente).
    """
    val_a = _obter_chave(servico_a, criterio)
    val_b = _obter_chave(servico_b, criterio)

    if val_a < val_b:
        res = -1
    elif val_a > val_b:
        res = 1
    else:
        # Critério de desempate determinístico por ID
        res = -1 if servico_a.id < servico_b.id else (1 if servico_a.id > servico_b.id else 0)

    return res if asc else -res


# ==============================================================================
# 1. MERGE SORT EM LISTA ENCADEADA (O(n log n))
# ==============================================================================

class MergeSortContador:
    def __init__(self):
        self.comparacoes = 0
        self.religacoes = 0


def _dividir_ao_meio(cabeca: Node) -> Tuple[Node, Node]:
    """
    Divide a lista encadeada ao meio usando o algoritmo dos ponteiros
    Lento e Rápido (Slow & Fast Pointer).
    """
    if cabeca is None or cabeca.proximo is None:
        return cabeca, None

    lento = cabeca
    rapido = cabeca.proximo

    while rapido is not None and rapido.proximo is not None:
        lento = lento.proximo
        rapido = rapido.proximo.proximo

    meio = lento.proximo
    lento.proximo = None  # Quebra o encadeamento dividindo a lista
    return cabeca, meio


def _intercalar(
    esq: Optional[Node],
    dir_: Optional[Node],
    criterio: str,
    asc: bool,
    contador: MergeSortContador
) -> Optional[Node]:
    """
    Intercala duas listas encadeadas já ordenadas religando os nós diretamente.
    """
    if esq is None:
        return dir_
    if dir_ is None:
        return esq

    # Nó sentinela (dummy node) para simplificar a cabeça da lista resultante
    dummy = Node(dado=None)
    cauda = dummy

    while esq is not None and dir_ is not None:
        contador.comparacoes += 1
        comp = _comparar(esq.dado, dir_.dado, criterio, asc)
        if comp <= 0:
            cauda.proximo = esq
            esq = esq.proximo
        else:
            cauda.proximo = dir_
            dir_ = dir_.proximo
        cauda = cauda.proximo
        contador.religacoes += 1

    if esq is not None:
        cauda.proximo = esq
        contador.religacoes += 1
    elif dir_ is not None:
        cauda.proximo = dir_
        contador.religacoes += 1

    return dummy.proximo


def _merge_sort_rec(
    cabeca: Optional[Node],
    criterio: str,
    asc: bool,
    contador: MergeSortContador
) -> Optional[Node]:
    """Recursão principal do Merge Sort."""
    if cabeca is None or cabeca.proximo is None:
        return cabeca

    esq, dir_ = _dividir_ao_meio(cabeca)
    esq_ordenado = _merge_sort_rec(esq, criterio, asc, contador)
    dir_ordenado = _merge_sort_rec(dir_, criterio, asc, contador)

    return _intercalar(esq_ordenado, dir_ordenado, criterio, asc, contador)


def merge_sort_lista(
    lista_original: ListaEncadeada,
    criterio: str = "id",
    asc: bool = True
) -> Tuple[ListaEncadeada, Dict[str, Any]]:
    """
    Executa o Merge Sort completo sobre uma cópia fiel da lista encadeada.
    Preserva a integridade da lista original.
    
    Complexidade:
    - Pior Caso: O(n log n)
    - Melhor Caso: O(n log n)
    - Caso Médio: O(n log n)
    - Espaço: O(log n) devido à pilha de recursão.
    """
    inicio_tempo = time.perf_counter()
    contador = MergeSortContador()

    # Criação de cópia com novos nós para não desestruturar a lista original
    nova_lista = ListaEncadeada()
    for servico in lista_original:
        novo_no = Node(dado=servico)
        if nova_lista.cabeca is None:
            nova_lista.cabeca = novo_no
        else:
            atual = nova_lista.cabeca
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no
        nova_lista._tamanho += 1

    if nova_lista.tamanho() > 1:
        nova_lista.cabeca = _merge_sort_rec(nova_lista.cabeca, criterio, asc, contador)

    fim_tempo = time.perf_counter()
    duracao_ms = (fim_tempo - inicio_tempo) * 1000

    metricas = {
        "algoritmo": "Merge Sort (Divisão & Conquista em Lista Encadeada)",
        "criterio": criterio,
        "ordem": "Crescente" if asc else "Decrescente",
        "comparacoes": contador.comparacoes,
        "religacoes_ponteiros": contador.religacoes,
        "elementos_ordenados": nova_lista.tamanho(),
        "tempo_execucao_ms": round(duracao_ms, 4)
    }

    return nova_lista, metricas


# ==============================================================================
# 2. INSERTION SORT EM LISTA ENCADEADA (O(n²))
# ==============================================================================

def insertion_sort_lista(
    lista_original: ListaEncadeada,
    criterio: str = "id",
    asc: bool = True
) -> Tuple[ListaEncadeada, Dict[str, Any]]:
    """
    Executa o Insertion Sort na lista encadeada.
    Insere elemento a elemento na posição ordenada correta.
    
    Complexidade:
    - Pior Caso: O(n²) - lista na ordem inversa.
    - Melhor Caso: O(n) - lista já ordenada.
    - Caso Médio: O(n²)
    - Espaço: O(1)
    """
    inicio_tempo = time.perf_counter()
    comparacoes = 0
    religacoes = 0

    nova_lista = ListaEncadeada()
    if lista_original.esta_vazia():
        return nova_lista, {
            "algoritmo": "Insertion Sort (Lista Encadeada)",
            "criterio": criterio,
            "ordem": "Crescente" if asc else "Decrescente",
            "comparacoes": 0,
            "religacoes_ponteiros": 0,
            "elementos_ordenados": 0,
            "tempo_execucao_ms": 0.0
        }

    cabeca_ordenada: Optional[Node] = None

    # Percorre cada elemento da lista original
    for servico in lista_original:
        no_inserir = Node(dado=servico)

        # Caso 1: a sublista ordenada está vazia ou o nó deve ser a nova cabeça
        if cabeca_ordenada is None:
            cabeca_ordenada = no_inserir
            religacoes += 1
        else:
            comparacoes += 1
            if _comparar(no_inserir.dado, cabeca_ordenada.dado, criterio, asc) < 0:
                no_inserir.proximo = cabeca_ordenada
                cabeca_ordenada = no_inserir
                religacoes += 1
            else:
                # Caso 2: percorre a sublista ordenada procurando o ponto correto
                atual = cabeca_ordenada
                while atual.proximo is not None:
                    comparacoes += 1
                    if _comparar(no_inserir.dado, atual.proximo.dado, criterio, asc) < 0:
                        break
                    atual = atual.proximo

                no_inserir.proximo = atual.proximo
                atual.proximo = no_inserir
                religacoes += 1

    nova_lista.cabeca = cabeca_ordenada
    nova_lista._tamanho = lista_original.tamanho()

    fim_tempo = time.perf_counter()
    duracao_ms = (fim_tempo - inicio_tempo) * 1000

    metricas = {
        "algoritmo": "Insertion Sort (Inserção Ordenada na Lista)",
        "criterio": criterio,
        "ordem": "Crescente" if asc else "Decrescente",
        "comparacoes": comparacoes,
        "religacoes_ponteiros": religacoes,
        "elementos_ordenados": nova_lista.tamanho(),
        "tempo_execucao_ms": round(duracao_ms, 4)
    }

    return nova_lista, metricas


# ==============================================================================
# 3. SELECTION SORT EM LISTA ENCADEADA (O(n²))
# ==============================================================================

def selection_sort_lista(
    lista_original: ListaEncadeada,
    criterio: str = "id",
    asc: bool = True
) -> Tuple[ListaEncadeada, Dict[str, Any]]:
    """
    Executa o Selection Sort criando uma nova lista encadeada ordenada nó a nó.
    Complexidade: O(n²) em todos os casos.
    """
    inicio_tempo = time.perf_counter()
    comparacoes = 0
    trocas = 0

    nova_lista = ListaEncadeada()
    elementos = lista_original.percurso()  # cópia de referências para seleção
    n = len(elementos)

    for i in range(n):
        indice_selecionado = i
        for j in range(i + 1, n):
            comparacoes += 1
            if _comparar(elementos[j], elementos[indice_selecionado], criterio, asc) < 0:
                indice_selecionado = j

        if indice_selecionado != i:
            elementos[i], elementos[indice_selecionado] = elementos[indice_selecionado], elementos[i]
            trocas += 1

        nova_lista.inserir_fim(elementos[i])

    fim_tempo = time.perf_counter()
    duracao_ms = (fim_tempo - inicio_tempo) * 1000

    metricas = {
        "algoritmo": "Selection Sort (Seleção Direta)",
        "criterio": criterio,
        "ordem": "Crescente" if asc else "Decrescente",
        "comparacoes": comparacoes,
        "religacoes_ponteiros": trocas,
        "elementos_ordenados": nova_lista.tamanho(),
        "tempo_execucao_ms": round(duracao_ms, 4)
    }

    return nova_lista, metricas


def executar_ordenacao(
    lista: ListaEncadeada,
    criterio: str = "id",
    algoritmo: str = "merge_sort",
    asc: bool = True
) -> Tuple[ListaEncadeada, Dict[str, Any]]:
    """
    Despachante flexível para executar o algoritmo de ordenação selecionado.
    """
    algo = algoritmo.lower().replace("-", "_").strip()
    if algo in ("merge", "mergesort", "merge_sort"):
        return merge_sort_lista(lista, criterio=criterio, asc=asc)
    elif algo in ("insertion", "insertionsort", "insertion_sort"):
        return insertion_sort_lista(lista, criterio=criterio, asc=asc)
    elif algo in ("selection", "selectionsort", "selection_sort"):
        return selection_sort_lista(lista, criterio=criterio, asc=asc)
    else:
        # Padrão: Merge Sort
        return merge_sort_lista(lista, criterio=criterio, asc=asc)

