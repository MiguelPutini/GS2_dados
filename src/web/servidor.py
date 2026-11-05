"""
Servidor Web HTTP nativo para o Citizen Assist AI.
Conecta diretamente à estrutura de dados ListaEncadeada e expõe API RESTful + Frontend.
Utiliza exclusivamente a biblioteca padrão do Python (sem dependências de terceiros).
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import mimetypes
from typing import Optional
from src.estruturas.lista_encadeada import ListaEncadeada
from src.modelos.servico import ServicoPublico
from src.algoritmos.busca import busca_linear_id, busca_linear_atributo
from src.algoritmos.ordenacao import merge_sort_lista, insertion_sort_lista, selection_sort_lista
from src.persistencia.repositorio import RepositorioServicos


PASTA_ESTATICOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estaticos")


class ManipuladorRequisicoes(http.server.SimpleHTTPRequestHandler):
    """
    Handler HTTP com suporte a endpoints de API RESTful conectada à Lista Encadeada.
    """

    lista_compartilhada: ListaEncadeada = None
    repositorio_compartilhado: RepositorioServicos = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PASTA_ESTATICOS, **kwargs)

    def _responder_json(self, status_code: int, dados: dict):
        payload = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        """Suporte a CORS pre-flight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Rota: Listar todos os serviços
        if path == "/api/servicos":
            servicos = [s.to_dict() for s in self.lista_compartilhada]
            self._responder_json(200, {
                "sucesso": True,
                "total": len(servicos),
                "servicos": servicos
            })
            return

        # Rota: Inspecionar topologia dos nós DSA
        if path == "/api/nos-dsa":
            nos = self.lista_compartilhada.inspecionar_ponteiros()
            self._responder_json(200, {
                "sucesso": True,
                "total_nos": len(nos),
                "cabeca_endereco": nos[0]["endereco_memoria_no"] if nos else "NULL",
                "nos": nos
            })
            return

        # Rota: Estatísticas e agregações
        if path == "/api/estatisticas":
            stats = self.lista_compartilhada.gerar_estatisticas()
            self._responder_json(200, {
                "sucesso": True,
                "estatisticas": stats
            })
            return

        # Rota: Busca por atributo
        if path == "/api/busca":
            campo = query.get("campo", ["geral"])[0]
            termo = query.get("termo", [""])[0]
            resultados, metricas = busca_linear_atributo(self.lista_compartilhada, campo=campo, termo=termo)
            self._responder_json(200, {
                "sucesso": True,
                "metricas": metricas,
                "resultados": [s.to_dict() for s in resultados]
            })
            return

        # Rota: Consultar por ID (/api/servicos/101)
        if path.startswith("/api/servicos/"):
            try:
                id_servico = int(path.split("/")[-1])
                servico, metricas = busca_linear_id(self.lista_compartilhada, id_servico)
                if servico:
                    self._responder_json(200, {
                        "sucesso": True,
                        "metricas": metricas,
                        "servico": servico.to_dict()
                    })
                else:
                    self._responder_json(404, {
                        "sucesso": False,
                        "metricas": metricas,
                        "mensagem": f"Serviço ID {id_servico} não encontrado."
                    })
            except ValueError:
                self._responder_json(400, {"sucesso": False, "mensagem": "ID inválido."})
            return

        # Se não for endpoint de API, serve arquivos estáticos (HTML, CSS, JS)
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        corpo = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            dados = json.loads(corpo) if corpo else {}
        except json.JSONDecodeError:
            self._responder_json(400, {"sucesso": False, "mensagem": "JSON inválido no corpo da requisição."})
            return

        # Rota: Cadastrar novo serviço
        if path == "/api/servicos":
            try:
                id_servico = int(dados.get("id", 0))
                if self.lista_compartilhada.existe_id(id_servico):
                    self._responder_json(409, {
                        "sucesso": False,
                        "mensagem": f"ID {id_servico} já existe na Lista Encadeada. Use outro identificador."
                    })
                    return

                novo = ServicoPublico.from_dict(dados)
                self.lista_compartilhada.inserir_fim(novo)
                self._responder_json(201, {
                    "sucesso": True,
                    "mensagem": f"Serviço ID {novo.id} cadastrado na Lista Encadeada com sucesso!",
                    "servico": novo.to_dict()
                })
            except Exception as e:
                self._responder_json(400, {"sucesso": False, "mensagem": str(e)})
            return

        # Rota: Ordenar lista com algoritmos DSA
        if path == "/api/ordenar":
            criterio = dados.get("criterio", "id")
            algoritmo = dados.get("algoritmo", "merge_sort")
            asc = bool(dados.get("asc", True))

            if algoritmo == "insertion_sort":
                lista_ord, metricas = insertion_sort_lista(self.lista_compartilhada, criterio=criterio, asc=asc)
            elif algoritmo == "selection_sort":
                lista_ord, metricas = selection_sort_lista(self.lista_compartilhada, criterio=criterio, asc=asc)
            else:
                lista_ord, metricas = merge_sort_lista(self.lista_compartilhada, criterio=criterio, asc=asc)

            # Aplica opcionalmente na lista oficial
            aplicar = bool(dados.get("aplicar_principal", False))
            if aplicar:
                ManipuladorRequisicoes.lista_compartilhada = lista_ord

            self._responder_json(200, {
                "sucesso": True,
                "metricas": metricas,
                "servicos": [s.to_dict() for s in lista_ord]
            })
            return

        # Rota: Restaurar dados originais (Reset)
        if path == "/api/resetar":
            self.lista_compartilhada.limpar()
            qtd = self.repositorio_compartilhado.carregar_para_lista(self.lista_compartilhada)
            self._responder_json(200, {
                "sucesso": True,
                "mensagem": f"Base reinicializada com {qtd} registros originais.",
                "total": self.lista_compartilhada.tamanho()
            })
            return

        self._responder_json(404, {"sucesso": False, "mensagem": "Endpoint não encontrado."})

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/servicos/"):
            try:
                id_servico = int(path.split("/")[-1])
                content_length = int(self.headers.get("Content-Length", 0))
                corpo = self.rfile.read(content_length).decode("utf-8")
                dados = json.loads(corpo)

                atualizado = self.lista_compartilhada.atualizar(id_servico, dados)
                if atualizado:
                    servico = self.lista_compartilhada.buscar_por_id(id_servico)
                    self._responder_json(200, {
                        "sucesso": True,
                        "mensagem": f"Serviço ID {id_servico} atualizado com sucesso.",
                        "servico": servico.to_dict()
                    })
                else:
                    self._responder_json(404, {
                        "sucesso": False,
                        "mensagem": f"Serviço ID {id_servico} não encontrado para atualização."
                    })
            except Exception as e:
                self._responder_json(400, {"sucesso": False, "mensagem": str(e)})
            return

        self._responder_json(404, {"sucesso": False, "mensagem": "Endpoint não encontrado."})

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/servicos/"):
            try:
                id_servico = int(path.split("/")[-1])
                removido = self.lista_compartilhada.remover_por_id(id_servico)
                if removido:
                    self._responder_json(200, {
                        "sucesso": True,
                        "mensagem": f"Serviço ID {id_servico} removido da Lista Encadeada e nós religados com sucesso.",
                        "removido": removido.to_dict()
                    })
                else:
                    self._responder_json(404, {
                        "sucesso": False,
                        "mensagem": f"Serviço ID {id_servico} não encontrado para exclusão."
                    })
            except Exception as e:
                self._responder_json(400, {"sucesso": False, "mensagem": str(e)})
            return

        self._responder_json(404, {"sucesso": False, "mensagem": "Endpoint não encontrado."})


def iniciar_servidor_web(lista: ListaEncadeada, porta: int = 8080):
    """
    Inicializa o servidor HTTP na porta especificada.
    """
    repositorio = RepositorioServicos()
    ManipuladorRequisicoes.lista_compartilhada = lista
    ManipuladorRequisicoes.repositorio_compartilhado = repositorio

    # Caso a lista esteja vazia ao iniciar, carrega dados iniciais
    if lista.esta_vazia():
        repositorio.carregar_para_lista(lista)

    endereco = ("", porta)
    with socketserver.TCPServer(endereco, ManipuladorRequisicoes) as httpd:
        print("=" * 75)
        print(f" Servidor Web Citizen Assist AI ativo em: http://localhost:{porta}")
        print(f" Integrado diretamente à Lista Encadeada em memória ({lista.tamanho()} nós).")
        print(" Pressione Ctrl+C para encerrar o servidor web.")
        print("=" * 75)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n Servidor web encerrado pelo usuário.")

