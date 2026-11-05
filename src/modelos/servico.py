"""
Modelo de dados para o Citizen Assist AI.
Representa um serviço ou orientação pública disponibilizada ao cidadão.
"""

from typing import Dict, Any


CATEGORIAS_VALIDAS = [
    "Saúde",
    "Assistência Social",
    "Documentação e Cidadania",
    "Educação e Qualificação",
    "Serviços Urbanos"
]

STATUS_VALIDOS = ["Ativo", "Em Atualização", "Suspenso"]


class ServicoPublico:
    """
    Entidade que representa um serviço público ou orientação ao cidadão.
    Contém validações de integridade dos campos.
    """

    def __init__(
        self,
        id_servico: int,
        titulo: str,
        categoria: str,
        descricao: str,
        requisitos: str,
        local_atendimento: str,
        publico_alvo: str = "População em geral",
        tempo_estimado_dias: int = 1,
        status: str = "Ativo"
    ):
        self.id = self._validar_id(id_servico)
        self.titulo = self._validar_texto(titulo, "Título")
        self.categoria = self._validar_categoria(categoria)
        self.descricao = self._validar_texto(descricao, "Descrição")
        self.requisitos = self._validar_texto(requisitos, "Requisitos")
        self.local_atendimento = self._validar_texto(local_atendimento, "Local de atendimento")
        self.publico_alvo = self._validar_texto(publico_alvo, "Público-alvo")
        self.tempo_estimado_dias = self._validar_tempo(tempo_estimado_dias)
        self.status = self._validar_status(status)

    @staticmethod
    def _validar_id(valor: Any) -> int:
        try:
            val_int = int(valor)
            if val_int <= 0:
                raise ValueError("O identificador (ID) deve ser um número inteiro positivo maior que zero.")
            return val_int
        except (TypeError, ValueError) as err:
            raise ValueError(f"ID inválido: {valor}. Deve ser um número inteiro positivo.") from err

    @staticmethod
    def _validar_texto(valor: Any, nome_campo: str) -> str:
        if not valor or not str(valor).strip():
            raise ValueError(f"O campo '{nome_campo}' é obrigatório e não pode ser vazio.")
        return str(valor).strip()

    @staticmethod
    def _validar_categoria(valor: Any) -> str:
        texto = ServicoPublico._validar_texto(valor, "Categoria")
        for cat in CATEGORIAS_VALIDAS:
            if cat.lower() == texto.lower():
                return cat
        # Se for nova categoria não mapeada, permite com capitalização limpa
        return texto

    @staticmethod
    def _validar_tempo(valor: Any) -> int:
        try:
            val = int(valor)
            if val < 0:
                raise ValueError("O tempo estimado não pode ser negativo.")
            return val
        except (TypeError, ValueError) as err:
            raise ValueError(f"Tempo estimado inválido: {valor}. Deve ser um número inteiro.") from err

    @staticmethod
    def _validar_status(valor: Any) -> str:
        texto = ServicoPublico._validar_texto(valor, "Status")
        for st in STATUS_VALIDOS:
            if st.lower() == texto.lower():
                return st
        return "Ativo"

    def to_dict(self) -> Dict[str, Any]:
        """Converte o objeto para um dicionário serializável."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "requisitos": self.requisitos,
            "local_atendimento": self.local_atendimento,
            "publico_alvo": self.publico_alvo,
            "tempo_estimado_dias": self.tempo_estimado_dias,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, dados: Dict[str, Any]) -> "ServicoPublico":
        """Reconstrói uma instância de ServicoPublico a partir de um dicionário."""
        return cls(
            id_servico=dados.get("id"),
            titulo=dados.get("titulo", ""),
            categoria=dados.get("categoria", ""),
            descricao=dados.get("descricao", ""),
            requisitos=dados.get("requisitos", ""),
            local_atendimento=dados.get("local_atendimento", ""),
            publico_alvo=dados.get("publico_alvo", "População em geral"),
            tempo_estimado_dias=dados.get("tempo_estimado_dias", 1),
            status=dados.get("status", "Ativo")
        )

    def __str__(self) -> str:
        return (
            f"[ID: {self.id:03d}] {self.titulo} | Categoria: {self.categoria} | "
            f"Status: {self.status} | Prazo: {self.tempo_estimado_dias} dia(s)\n"
            f"   Local: {self.local_atendimento}\n"
            f"   Público: {self.publico_alvo}\n"
            f"   Requisitos: {self.requisitos}\n"
            f"   Descrição: {self.descricao}"
        )

