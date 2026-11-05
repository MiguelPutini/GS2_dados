"""
Módulo que define o Nó (Node) da Lista Encadeada.
Cada nó armazena uma referência ao dado (ServicoPublico) e um ponteiro/referência
para o próximo nó da lista encadeada.
"""

from typing import Optional, Any


class Node:
    """
    Nó de uma lista simplesmente encadeada.
    """

    def __init__(self, dado: Any, proximo: Optional["Node"] = None):
        self.dado = dado
        self.proximo: Optional["Node"] = proximo

    def __repr__(self) -> str:
        dado_id = getattr(self.dado, "id", str(self.dado))
        prox_id = getattr(self.proximo.dado, "id", "None") if self.proximo else "None"
        return f"Node(ID={dado_id} -> Prox={prox_id})"

