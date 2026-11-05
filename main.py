"""
Ponto de entrada principal do projeto Citizen Assist AI.
Global Solution 2026.2 - Data Structures and Algorithms (DSA).
"""

import sys
import os

# Adiciona o diretório base ao sys.path para garantir importações relativas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.estruturas.lista_encadeada import ListaEncadeada
from src.persistencia.repositorio import RepositorioServicos
from src.cli.menu import MenuCLI


def main():
    print("=" * 75)
    print("  Iniciando Citizen Assist AI | Estruturas de Dados e Algoritmos")
    print("=" * 75)

    # Inicializa a estrutura de dados central da equipe: Lista Encadeada
    lista = ListaEncadeada()
    repositorio = RepositorioServicos()

    # Carga automática dos registros de exemplo para permitir teste imediato
    qtd = repositorio.carregar_para_lista(lista)
    print(f"[*] Base inicial carregada: {qtd} serviços públicos prontos para consulta.")

    # Inicializa a interface de menu interativo no terminal
    menu = MenuCLI(lista=lista)
    try:
        menu.executar()
    except KeyboardInterrupt:
        print("\n\n[!] Execução interrompida pelo usuário via teclado (Ctrl+C). Saindo...")
        sys.exit(0)


if __name__ == "__main__":
    main()

