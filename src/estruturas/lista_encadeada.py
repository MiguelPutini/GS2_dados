"""
Implementação de Lista Simplesmente Encadeada para o Citizen Assist AI.
Não utiliza estruturas de array para armazenamento: os elementos são conectados
exclusivamente através das referências entre instâncias da classe Node.
"""

from typing import Optional, List, Dict, Any, Iterator
from src.estruturas.no import Node
from src.modelos.servico import ServicoPublico


class ListaEncadeada:
    """
    Estrutura de dados Lista Simplesmente Encadeada (Singly Linked List).
    Armazena e gerencia nós contendo instâncias de ServicoPublico.
    """

    def __init__(self):
        self.cabeca: Optional[Node] = None
        self._tamanho: int = 0

    def esta_vazia(self) -> bool:
        """Verifica se a lista encadeada está vazia."""
        return self.cabeca is None

    def tamanho(self) -> int:
        """Retorna o número de elementos atualmente armazenados na lista."""
        return self._tamanho

    def existe_id(self, id_servico: int) -> bool:
        """Verifica se já existe algum serviço com o ID fornecido."""
        atual = self.cabeca
        while atual is not None:
            if atual.dado.id == id_servico:
                return True
            atual = atual.proximo
        return False

    def inserir_inicio(self, servico: ServicoPublico) -> None:
        """
        Insere um novo elemento no início da lista encadeada.
        Complexidade de tempo: O(1)
        """
        if self.existe_id(servico.id):
            raise ValueError(f"Conflito de chave única: já existe um serviço cadastrado com o ID {servico.id}.")

        novo_no = Node(dado=servico, proximo=self.cabeca)
        self.cabeca = novo_no
        self._tamanho += 1

    def inserir_fim(self, servico: ServicoPublico) -> None:
        """
        Insere um novo elemento no final da lista encadeada.
        Complexidade de tempo: O(n) percorrendo até o último nó.
        """
        if self.existe_id(servico.id):
            raise ValueError(f"Conflito de chave única: já existe um serviço cadastrado com o ID {servico.id}.")

        novo_no = Node(dado=servico, proximo=None)
        if self.cabeca is None:
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no

        self._tamanho += 1

    def inserir(self, servico: ServicoPublico) -> None:
        """Método padrão de inserção (insere no fim da lista)."""
        self.inserir_fim(servico)

    def buscar_por_id(self, id_servico: int) -> Optional[ServicoPublico]:
        """
        Busca sequencial por identificador único.
        Complexidade de tempo: O(n)
        Retorna o objeto ServicoPublico correspondente ou None se não encontrado.
        """
        atual = self.cabeca
        while atual is not None:
            if atual.dado.id == id_servico:
                return atual.dado
            atual = atual.proximo
        return None

    def remover_por_id(self, id_servico: int) -> Optional[ServicoPublico]:
        """
        Remove o nó cujo serviço possui o identificador informado.
        Ajusta os ponteiros garantindo a integridade da lista.
        Complexidade de tempo: O(n)
        Retorna o ServicoPublico removido ou None se não for encontrado.
        """
        if self.cabeca is None:
            return None

        # Caso especial: o nó a remover é a cabeça da lista
        if self.cabeca.dado.id == id_servico:
            removido = self.cabeca.dado
            self.cabeca = self.cabeca.proximo
            self._tamanho -= 1
            return removido

        # Percorrer procurando o antecessor do nó a remover
        anterior = self.cabeca
        atual = self.cabeca.proximo

        while atual is not None:
            if atual.dado.id == id_servico:
                removido = atual.dado
                anterior.proximo = atual.proximo
                atual.proximo = None  # Desconecta referência
                self._tamanho -= 1
                return removido
            anterior = atual
            atual = atual.proximo

        return None

    def atualizar(self, id_servico: int, novos_dados: Dict[str, Any]) -> bool:
        """
        Atualiza os campos de um registro existente mantendo o mesmo ID.
        """
        servico = self.buscar_por_id(id_servico)
        if servico is None:
            return False

        if "titulo" in novos_dados and novos_dados["titulo"]:
            servico.titulo = ServicoPublico._validar_texto(novos_dados["titulo"], "Título")
        if "categoria" in novos_dados and novos_dados["categoria"]:
            servico.categoria = ServicoPublico._validar_categoria(novos_dados["categoria"])
        if "descricao" in novos_dados and novos_dados["descricao"]:
            servico.descricao = ServicoPublico._validar_texto(novos_dados["descricao"], "Descrição")
        if "requisitos" in novos_dados and novos_dados["requisitos"]:
            servico.requisitos = ServicoPublico._validar_texto(novos_dados["requisitos"], "Requisitos")
        if "local_atendimento" in novos_dados and novos_dados["local_atendimento"]:
            servico.local_atendimento = ServicoPublico._validar_texto(novos_dados["local_atendimento"], "Local de atendimento")
        if "publico_alvo" in novos_dados and novos_dados["publico_alvo"]:
            servico.publico_alvo = ServicoPublico._validar_texto(novos_dados["publico_alvo"], "Público-alvo")
        if "tempo_estimado_dias" in novos_dados and novos_dados["tempo_estimado_dias"] is not None:
            servico.tempo_estimado_dias = ServicoPublico._validar_tempo(novos_dados["tempo_estimado_dias"])
        if "status" in novos_dados and novos_dados["status"]:
            servico.status = ServicoPublico._validar_status(novos_dados["status"])

        return True

    def percurso(self) -> List[ServicoPublico]:
        """
        Realiza o percurso completo da lista encadeada da cabeça até o fim,
        retornando uma lista Python contendo as referências dos serviços.
        Não altera os nós originais.
        """
        resultado: List[ServicoPublico] = []
        atual = self.cabeca
        while atual is not None:
            resultado.append(atual.dado)
            atual = atual.proximo
        return resultado

    def __iter__(self) -> Iterator[ServicoPublico]:
        """Permite iterar sobre a lista encadeada usando loops for."""
        atual = self.cabeca
        while atual is not None:
            yield atual.dado
            atual = atual.proximo

    def limpar(self) -> None:
        """Esvazia a lista encadeada."""
        self.cabeca = None
        self._tamanho = 0

    def gerar_estatisticas(self) -> Dict[str, Any]:
        """
        Produz informações analíticas e estatísticas úteis sobre os serviços:
        - Total de registros
        - Contagem por categoria
        - Distribuição percentual por categoria
        - Contagem por status
        - Tempo médio estimado de atendimento
        """
        total = self._tamanho
        if total == 0:
            return {
                "total_registros": 0,
                "por_categoria": {},
                "distribuicao_percentual": {},
                "por_status": {},
                "tempo_medio_dias": 0.0
            }

        por_categoria: Dict[str, int] = {}
        por_status: Dict[str, int] = {}
        soma_tempo = 0

        atual = self.cabeca
        while atual is not None:
            s = atual.dado
            por_categoria[s.categoria] = por_categoria.get(s.categoria, 0) + 1
            por_status[s.status] = por_status.get(s.status, 0) + 1
            soma_tempo += s.tempo_estimado_dias
            atual = atual.proximo

        distribuicao_percentual = {
            cat: round((qtd / total) * 100, 2)
            for cat, qtd in por_categoria.items()
        }

        return {
            "total_registros": total,
            "por_categoria": por_categoria,
            "distribuicao_percentual": distribuicao_percentual,
            "por_status": por_status,
            "tempo_medio_dias": round(soma_tempo / total, 2)
        }

    def inspecionar_ponteiros(self) -> List[Dict[str, Any]]:
        """
        Retorna a estrutura explícita dos nós e referências para fins didáticos,
        demonstração prática e visualização gráfica.
        """
        nos_info = []
        atual = self.cabeca
        indice = 0
        while atual is not None:
            proximo_id = atual.proximo.dado.id if atual.proximo else None
            nos_info.append({
                "indice": indice,
                "id": atual.dado.id,
                "titulo": atual.dado.titulo,
                "categoria": atual.dado.categoria,
                "proximo_id": proximo_id,
                "endereco_memoria_no": hex(id(atual)),
                "endereco_memoria_prox": hex(id(atual.proximo)) if atual.proximo else "NULL"
            })
            indice += 1
            atual = atual.proximo
        return nos_info

