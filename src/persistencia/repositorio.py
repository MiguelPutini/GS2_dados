"""
Camada de persistência para o Citizen Assist AI.
Lê e grava registros em arquivo JSON, preenchendo a Lista Encadeada.
"""

import json
import os
from typing import Optional
from src.estruturas.lista_encadeada import ListaEncadeada
from src.modelos.servico import ServicoPublico


CAMINHO_PADRAO = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "dados",
    "servicos_iniciais.json"
)


class RepositorioServicos:
    """
    Gerenciador de carga e persistência da Lista Encadeada.
    """

    def __init__(self, caminho_arquivo: Optional[str] = None):
        self.caminho_arquivo = caminho_arquivo or CAMINHO_PADRAO

    def carregar_para_lista(self, lista: ListaEncadeada) -> int:
        """
        Carrega os registros do arquivo JSON e insere na Lista Encadeada.
        Retorna a quantidade de registros carregados com sucesso.
        """
        if not os.path.exists(self.caminho_arquivo):
            return 0

        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)

            carregados = 0
            for item in dados:
                try:
                    servico = ServicoPublico.from_dict(item)
                    if not lista.existe_id(servico.id):
                        lista.inserir_fim(servico)
                        carregados += 1
                except Exception as err:
                    print(f"[Aviso] Registro ignorado por inconformidade: {err}")

            return carregados
        except Exception as e:
            print(f"[Erro ao carregar dados]: {e}")
            return 0

    def salvar_da_lista(self, lista: ListaEncadeada, caminho_destino: Optional[str] = None) -> bool:
        """
        Exporta todos os elementos percorridos da Lista Encadeada para JSON.
        """
        destino = caminho_destino or self.caminho_arquivo
        try:
            pasta = os.path.dirname(destino)
            if pasta and not os.path.exists(pasta):
                os.makedirs(pasta, exist_ok=True)

            registros = [servico.to_dict() for servico in lista]
            with open(destino, "w", encoding="utf-8") as f:
                json.dump(registros, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[Erro ao salvar dados]: {e}")
            return False

