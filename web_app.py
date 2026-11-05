"""
Iniciador do Portal Web Citizen Assist AI.
Atende à funcionalidade adicional opcional de interface Web/gráfica
sem violar nenhum dos requisitos estruturais de DSA (Lista Encadeada pura).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.estruturas.lista_encadeada import ListaEncadeada
from src.persistencia.repositorio import RepositorioServicos
from src.web.servidor import iniciar_servidor_web


def main():
    porta = 8080
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        porta = int(sys.argv[1])

    lista = ListaEncadeada()
    repositorio = RepositorioServicos()
    repositorio.carregar_para_lista(lista)

    iniciar_servidor_web(lista, porta=porta)


if __name__ == "__main__":
    main()

