"""
Implementações próprias de algoritmos de busca para o Citizen Assist AI.
Não utiliza funções utilitárias ou bibliotecas externas.
"""

from typing import List, Optional, Tuple, Dict, Any
from src.estruturas.lista_encadeada import ListaEncadeada
from src.modelos.servico import ServicoPublico


def busca_linear_id(
    lista: ListaEncadeada,
    id_procurado: int
) -> Tuple[Optional[ServicoPublico], Dict[str, Any]]:
    """
    Realiza Busca Linear sobre a lista encadeada à procura de um ID específico.
    
    Complexidade:
    - Pior Caso: O(n) - o elemento está no último nó ou não existe.
    - Melhor Caso: O(1) - o elemento está na cabeça da lista.
    - Espaço: O(1) - memória auxiliar constante.
    
    Retorna:
    (servico_encontrado_ou_None, estatisticas_da_busca)
    """
    comparacoes = 0
    atual = lista.cabeca

    while atual is not None:
        comparacoes += 1
        if atual.dado.id == id_procurado:
            return atual.dado, {
                "algoritmo": "Busca Linear por ID",
                "comparacoes": comparacoes,
                "encontrado": True,
                "motivo": f"Serviço com ID {id_procurado} localizado após {comparacoes} comparação(ões)."
            }
        atual = atual.proximo

    return None, {
        "algoritmo": "Busca Linear por ID",
        "comparacoes": comparacoes,
        "encontrado": False,
        "motivo": f"Nenhum registro com ID {id_procurado} foi localizado na lista (total de comparações: {comparacoes})."
    }


def busca_linear_atributo(
    lista: ListaEncadeada,
    campo: str,
    termo: str
) -> Tuple[List[ServicoPublico], Dict[str, Any]]:
    """
    Realiza Busca Linear na lista encadeada buscando por um atributo (ex: 'titulo' ou 'categoria').
    Suporta busca por substring de forma case-insensitive.
    
    Complexidade:
    - Pior Caso: O(n) - percorre todos os nós para coletar todas as correspondências.
    - Melhor Caso: O(n) - como pode haver múltiplos resultados, deve inspecionar toda a lista.
    - Espaço: O(k) onde k é o número de registros encontrados.
    """
    if not termo or not termo.strip():
        return [], {
            "algoritmo": "Busca Linear por Atributo",
            "comparacoes": 0,
            "encontrado": False,
            "motivo": "O termo de busca não pode ser vazio."
        }

    termo_limpo = termo.strip().lower()
    resultados: List[ServicoPublico] = []
    comparacoes = 0
    atual = lista.cabeca

    while atual is not None:
        comparacoes += 1
        servico = atual.dado

        if campo == "categoria":
            # Correspondência no campo categoria
            if termo_limpo in servico.categoria.lower():
                resultados.append(servico)
        elif campo == "titulo":
            # Correspondência no título
            if termo_limpo in servico.titulo.lower():
                resultados.append(servico)
        elif campo == "geral":
            # Busca textual ampla em título, descrição e requisitos
            if (
                termo_limpo in servico.titulo.lower()
                or termo_limpo in servico.categoria.lower()
                or termo_limpo in servico.descricao.lower()
                or termo_limpo in servico.requisitos.lower()
            ):
                resultados.append(servico)
        else:
            # Padrão: título
            if termo_limpo in servico.titulo.lower():
                resultados.append(servico)

        atual = atual.proximo

    encontrado = len(resultados) > 0
    motivo = (
        f"Foram encontrados {len(resultados)} registro(s) para o termo '{termo}' no campo '{campo}'."
        if encontrado else
        f"Nenhum registro encontrado para o termo '{termo}' no campo '{campo}' após examinar {comparacoes} nó(s)."
    )

    return resultados, {
        "algoritmo": "Busca Linear por Atributo",
        "campo": campo,
        "termo": termo,
        "comparacoes": comparacoes,
        "total_encontrados": len(resultados),
        "encontrado": encontrado,
        "motivo": motivo
    }


def busca_binaria_em_vetor(
    servicos_ordenados: List[ServicoPublico],
    id_procurado: int
) -> Tuple[Optional[ServicoPublico], Dict[str, Any]]:
    """
    Implementação própria de Busca Binária aplicada sobre uma sequência já ordenada por ID.
    Demonstra a diferença analítica entre busca em acesso indexado O(log n) vs sequencial O(n).
    
    Complexidade:
    - Pior Caso: O(log n)
    - Melhor Caso: O(1)
    - Espaço: O(1)
    """
    inicio = 0
    fim = len(servicos_ordenados) - 1
    comparacoes = 0

    while inicio <= fim:
        comparacoes += 1
        meio = (inicio + fim) // 2
        servico_atual = servicos_ordenados[meio]

        if servico_atual.id == id_procurado:
            return servico_atual, {
                "algoritmo": "Busca Binária (Vetor Ordenado)",
                "comparacoes": comparacoes,
                "encontrado": True,
                "motivo": f"Serviço ID {id_procurado} encontrado na posição {meio} com apenas {comparacoes} divisões binárias."
            }
        elif servico_atual.id < id_procurado:
            inicio = meio + 1
        else:
            fim = meio - 1

    return None, {
        "algoritmo": "Busca Binária (Vetor Ordenado)",
        "comparacoes": comparacoes,
        "encontrado": False,
        "motivo": f"ID {id_procurado} não encontrado após {comparacoes} comparações binárias."
    }

