"""
Interface de Linha de Comando (CLI) para o Citizen Assist AI.
Implementa o menu interativo e validação rigorosa de entradas exigida pelo edital.
"""

import sys
from typing import Optional
from src.estruturas.lista_encadeada import ListaEncadeada
from src.modelos.servico import ServicoPublico, CATEGORIAS_VALIDAS, STATUS_VALIDOS
from src.algoritmos.busca import busca_linear_id, busca_linear_atributo, busca_binaria_em_vetor
from src.algoritmos.ordenacao import merge_sort_lista, insertion_sort_lista, selection_sort_lista
from src.persistencia.repositorio import RepositorioServicos


class MenuCLI:
    """
    Controlador do menu textual do sistema.
    """

    def __init__(self, lista: Optional[ListaEncadeada] = None):
        self.lista = lista if lista is not None else ListaEncadeada()
        self.repositorio = RepositorioServicos()

    def limpar_tela_ou_separador(self):
        print("\n" + "=" * 75)

    def ler_inteiro(self, prompt: str, minimo: Optional[int] = None, maximo: Optional[int] = None) -> int:
        """Lê um inteiro com validação contínua contra entradas não numéricas e limites."""
        while True:
            try:
                entrada = input(prompt).strip()
                if not entrada:
                    print(" [!] Entrada vazia. Digite um número válido.")
                    continue
                valor = int(entrada)
                if minimo is not None and valor < minimo:
                    print(f" [!] O valor deve ser maior ou igual a {minimo}.")
                    continue
                if maximo is not None and valor > maximo:
                    print(f" [!] O valor deve ser menor ou igual a {maximo}.")
                    continue
                return valor
            except ValueError:
                print(" [!] Entrada inválida. Por favor, digite um número inteiro.")

    def ler_texto(self, prompt: str, obrigatorio: bool = True) -> str:
        """Lê uma string garantindo que não seja vazia se for obrigatória."""
        while True:
            entrada = input(prompt).strip()
            if obrigatorio and not entrada:
                print(" [!] Este campo é obrigatório e não pode ser deixado em branco.")
                continue
            return entrada

    def selecionar_categoria(self) -> str:
        """Permite ao usuário escolher a categoria entre as válidas."""
        print("\nCategorias disponíveis:")
        for idx, cat in enumerate(CATEGORIAS_VALIDAS, 1):
            print(f"  [{idx}] {cat}")
        opcao = self.ler_inteiro("Selecione o número da categoria: ", minimo=1, maximo=len(CATEGORIAS_VALIDAS))
        return CATEGORIAS_VALIDAS[opcao - 1]

    def selecionar_status(self) -> str:
        """Permite ao usuário escolher o status."""
        print("\nStatus disponíveis:")
        for idx, st in enumerate(STATUS_VALIDOS, 1):
            print(f"  [{idx}] {st}")
        opcao = self.ler_inteiro("Selecione o status: ", minimo=1, maximo=len(STATUS_VALIDOS))
        return STATUS_VALIDOS[opcao - 1]

    # ==========================================================================
    # OPERAÇÕES DO MENU
    # ==========================================================================

    def op_cadastrar(self):
        """Operação 1: Cadastrar novo serviço com verificação de chave única."""
        self.limpar_tela_ou_separador()
        print("  >>> CADASTRO DE NOVO SERVIÇO / ORIENTAÇÃO PÚBLICA <<<")
        print("=" * 75)

        id_servico = self.ler_inteiro("Digite o ID único do serviço (ex: 201): ", minimo=1)
        if self.lista.existe_id(id_servico):
            print(f"\n [ERRO] Já existe um serviço cadastrado com o ID {id_servico}!")
            print(" Operação cancelada para preservar a integridade da chave primária.")
            return

        titulo = self.ler_texto("Título do serviço (ex: Emissão de Passe Livre): ")
        categoria = self.selecionar_categoria()
        descricao = self.ler_texto("Descrição detalhada: ")
        requisitos = self.ler_texto("Requisitos e documentos necessários: ")
        local = self.ler_texto("Local de atendimento ou canal de acesso: ")
        publico = self.ler_texto("Público-alvo (Pressione Enter para 'População em geral'): ", obrigatorio=False)
        if not publico:
            publico = "População em geral"
        tempo = self.ler_inteiro("Prazo estimado em dias úteis (ex: 5): ", minimo=0)
        status = self.selecionar_status()

        novo_servico = ServicoPublico(
            id_servico=id_servico,
            titulo=titulo,
            categoria=categoria,
            descricao=descricao,
            requisitos=requisitos,
            local_atendimento=local,
            publico_alvo=publico,
            tempo_estimado_dias=tempo,
            status=status
        )

        self.lista.inserir_fim(novo_servico)
        print(f"\n [SUCESSO] Serviço cadastrado com sucesso na Lista Encadeada!")
        print(f" Total atual de registros na lista: {self.lista.tamanho()}")

    def op_consultar_por_id(self):
        """Operação 2: Consultar registro por ID com detalhes do algoritmo."""
        self.limpar_tela_ou_separador()
        print("  >>> CONSULTA DE SERVIÇO POR IDENTIFICADOR (ID) <<<")
        print("=" * 75)

        if self.lista.esta_vazia():
            print(" [AVISO] A lista encadeada está vazia. Não há registros a consultar.")
            return

        id_procurado = self.ler_inteiro("Digite o ID do serviço que deseja consultar: ", minimo=1)
        servico, metricas = busca_linear_id(self.lista, id_procurado)

        print("\n" + "-" * 75)
        print(f" Resultado da Busca ({metricas['algoritmo']}):")
        print(f" Comparações realizadas: {metricas['comparacoes']}")
        print(f" Mensagem: {metricas['motivo']}")
        print("-" * 75)

        if servico:
            print("\n DETALHES DO REGISTRO:")
            print(f" ID:                  {servico.id}")
            print(f" Título:              {servico.titulo}")
            print(f" Categoria:           {servico.categoria}")
            print(f" Status:              {servico.status}")
            print(f" Prazo Estimado:      {servico.tempo_estimado_dias} dia(s)")
            print(f" Local:               {servico.local_atendimento}")
            print(f" Público-Alvo:        {servico.publico_alvo}")
            print(f" Requisitos:          {servico.requisitos}")
            print(f" Descrição:           {servico.descricao}")
        else:
            print(f" [!] Nenhum serviço encontrado com o identificador {id_procurado}.")

    def op_pesquisar_atributo(self):
        """Operação 3: Pesquisar por título ou categoria com algoritmo de busca."""
        self.limpar_tela_ou_separador()
        print("  >>> PESQUISA DE SERVIÇOS POR ATRIBUTO <<<")
        print("=" * 75)

        if self.lista.esta_vazia():
            print(" [AVISO] A lista encadeada está vazia. Não há registros a pesquisar.")
            return

        print("Escolha o atributo para pesquisa:")
        print(" [1] Pesquisar por TÍTULO")
        print(" [2] Pesquisar por CATEGORIA")
        print(" [3] Pesquisa Geral (Título, Categoria, Descrição, Requisitos)")
        opcao = self.ler_inteiro("Opção: ", minimo=1, maximo=3)

        campo_map = {1: "titulo", 2: "categoria", 3: "geral"}
        campo = campo_map[opcao]

        termo = self.ler_texto(f"Digite o termo de busca para '{campo}': ")
        resultados, metricas = busca_linear_atributo(self.lista, campo=campo, termo=termo)

        print("\n" + "-" * 75)
        print(f" Relatório da Busca ({metricas['algoritmo']}):")
        print(f" Campo: {campo} | Termo buscado: '{termo}'")
        print(f" Comparações de nós realizadas: {metricas['comparacoes']}")
        print(f" Total de correspondências encontradas: {len(resultados)}")
        print(f" Status: {metricas['motivo']}")
        print("-" * 75)

        if resultados:
            for s in resultados:
                print(f"\n -> [ID {s.id:03d}] {s.titulo}")
                print(f"    Categoria: {s.categoria} | Status: {s.status} | Prazo: {s.tempo_estimado_dias}d")
                print(f"    Local: {s.local_atendimento}")
                print(f"    Descrição: {s.descricao[:110]}...")
        else:
            print(" [!] Nenhum registro correspondeu aos critérios informados.")

    def op_listar_todos(self):
        """Operação 4: Listar todos os serviços na ordem atual do encadeamento."""
        self.limpar_tela_ou_separador()
        print("  >>> LISTAGEM GERAL DE SERVIÇOS (PERCURSO DA LISTA ENCADEADA) <<<")
        print("=" * 75)

        if self.lista.esta_vazia():
            print(" [AVISO] A lista encadeada está vazia no momento.")
            return

        print(f" Total de registros encadeados: {self.lista.tamanho()}\n")
        print(f"{'ID':<6} | {'TÍTULO':<35} | {'CATEGORIA':<22} | {'PRAZO':<6} | {'STATUS'}")
        print("-" * 80)

        for s in self.lista:
            titulo_resumido = (s.titulo[:32] + "...") if len(s.titulo) > 35 else s.titulo
            print(f"{s.id:<6} | {titulo_resumido:<35} | {s.categoria:<22} | {s.tempo_estimado_dias:>2} d  | {s.status}")

    def op_atualizar(self):
        """Operação 5: Atualizar campos de um serviço existente preservando integridade."""
        self.limpar_tela_ou_separador()
        print("  >>> ATUALIZAÇÃO DE SERVIÇO EXISTENTE <<<")
        print("=" * 75)

        if self.lista.esta_vazia():
            print(" [AVISO] A lista encadeada está vazia. Não há serviços para atualizar.")
            return

        id_procurado = self.ler_inteiro("Digite o ID do serviço que deseja atualizar: ", minimo=1)
        servico = self.lista.buscar_por_id(id_procurado)

        if not servico:
            print(f" [ERRO] Serviço com ID {id_procurado} não foi encontrado na lista!")
            return

        print(f"\nEditando o serviço: [ID {servico.id}] {servico.titulo}")
        print("Dica: Deixe o campo em branco (pressione Enter) para manter o valor atual.")

        novo_titulo = input(f"Novo Título [{servico.titulo}]: ").strip()
        print(f"Categoria atual: {servico.categoria}")
        alterar_cat = input("Deseja alterar a categoria? (s/N): ").strip().lower()
        nova_categoria = self.selecionar_categoria() if alterar_cat == "s" else servico.categoria

        nova_desc = input(f"Nova Descrição [{servico.descricao[:40]}...]: ").strip()
        novos_req = input(f"Novos Requisitos [{servico.requisitos[:40]}...]: ").strip()
        novo_local = input(f"Novo Local [{servico.local_atendimento}]: ").strip()
        novo_publico = input(f"Novo Público [{servico.publico_alvo}]: ").strip()

        novo_tempo_str = input(f"Novo Prazo em dias [{servico.tempo_estimado_dias}]: ").strip()
        novo_tempo = int(novo_tempo_str) if novo_tempo_str.isdigit() else servico.tempo_estimado_dias

        print(f"Status atual: {servico.status}")
        alterar_st = input("Deseja alterar o status? (s/N): ").strip().lower()
        novo_status = self.selecionar_status() if alterar_st == "s" else servico.status

        novos_dados = {
            "titulo": novo_titulo or servico.titulo,
            "categoria": nova_categoria,
            "descricao": nova_desc or servico.descricao,
            "requisitos": novos_req or servico.requisitos,
            "local_atendimento": novo_local or servico.local_atendimento,
            "publico_alvo": novo_publico or servico.publico_alvo,
            "tempo_estimado_dias": novo_tempo,
            "status": novo_status
        }

        self.lista.atualizar(id_procurado, novos_dados)
        print(f"\n [SUCESSO] Serviço ID {id_procurado} atualizado com êxito!")

    def op_excluir(self):
        """Operação 6: Excluir serviço com confirmação e preservação dos nós."""
        self.limpar_tela_ou_separador()
        print("  >>> EXCLUSÃO DE SERVIÇO <<<")
        print("=" * 75)

        if self.lista.esta_vazia():
            print(" [AVISO] A lista encadeada está vazia. Não há registros para excluir.")
            return

        id_procurado = self.ler_inteiro("Digite o ID do serviço que deseja excluir: ", minimo=1)
        servico = self.lista.buscar_por_id(id_procurado)

        if not servico:
            print(f" [!] Nenhum serviço encontrado com o ID {id_procurado}.")
            return

        print(f"\nRegistro a ser removido:")
        print(f" ID: {servico.id} - {servico.titulo} ({servico.categoria})")
        confirma = input("\nTem certeza que deseja excluir este registro? (s/N): ").strip().lower()

        if confirma == "s":
            removido = self.lista.remover_por_id(id_procurado)
            if removido:
                print(f" [SUCESSO] Serviço ID {id_procurado} removido e referências dos nós reajustadas.")
                print(f" Novo tamanho da lista encadeada: {self.lista.tamanho()}")
            else:
                print(" [!] Falha ao remover da lista encadeada.")
        else:
            print(" [CANCELADO] Operação de exclusão abortada pelo usuário.")

    def op_ordenar(self):
        """Operação 7: Ordenação própria estudada em DSA (Merge Sort, Insertion Sort, Selection Sort)."""
        self.limpar_tela_ou_separador()
        print("  >>> ORDENAÇÃO DE REGISTROS (ALGORITMOS DSA PRÓPRIOS) <<<")
        print("=" * 75)

        if self.lista.esta_vazia():
            print(" [AVISO] A lista encadeada está vazia. Impossível ordenar.")
            return

        print("Critérios de ordenação disponíveis:")
        print(" [1] Por IDENTIFICADOR (ID)")
        print(" [2] Por TÍTULO")
        print(" [3] Por CATEGORIA")
        print(" [4] Por PRAZO ESTIMADO (Tempo em dias)")
        opcao_crit = self.ler_inteiro("Selecione o critério: ", minimo=1, maximo=4)
        criterios = {1: "id", 2: "titulo", 3: "categoria", 4: "prazo"}
        criterio = criterios[opcao_crit]

        print("\nAlgoritmos de ordenação implementados (sem funções nativas):")
        print(" [1] Merge Sort       - O(n log n) [Divisão & Conquista ideal para listas encadeadas]")
        print(" [2] Insertion Sort   - O(n²)      [Inserção ordenada nó a nó]")
        print(" [3] Selection Sort   - O(n²)      [Seleção sucessiva do menor elemento]")
        opcao_algo = self.ler_inteiro("Selecione o algoritmo: ", minimo=1, maximo=3)

        print("\nOrdem:")
        print(" [1] Crescente (A-Z / Menor para Maior)")
        print(" [2] Decrescente (Z-A / Maior para Menor)")
        opcao_ordem = self.ler_inteiro("Selecione a ordem: ", minimo=1, maximo=2)
        asc = (opcao_ordem == 1)

        if opcao_algo == 1:
            lista_ordenada, metricas = merge_sort_lista(self.lista, criterio=criterio, asc=asc)
        elif opcao_algo == 2:
            lista_ordenada, metricas = insertion_sort_lista(self.lista, criterio=criterio, asc=asc)
        else:
            lista_ordenada, metricas = selection_sort_lista(self.lista, criterio=criterio, asc=asc)

        print("\n" + "=" * 75)
        print(" RELATÓRIO DE EXECUÇÃO DO ALGORITMO:")
        print(f" Algoritmo utilizado:      {metricas['algoritmo']}")
        print(f" Critério avaliado:        {metricas['criterio'].upper()} ({metricas['ordem']})")
        print(f" Elementos processados:    {metricas['elementos_ordenados']}")
        print(f" Comparações de chaves:    {metricas['comparacoes']}")
        print(f" Religações de ponteiros:  {metricas['religacoes_ponteiros']}")
        print(f" Tempo de execução:        {metricas['tempo_execucao_ms']} ms")
        print("=" * 75)

        print("\n RESULTADO DA LISTA ORDENADA:")
        print(f"{'ID':<6} | {'TÍTULO':<35} | {'CATEGORIA':<22} | {'PRAZO':<6} | {'STATUS'}")
        print("-" * 80)
        for s in lista_ordenada:
            titulo_resumido = (s.titulo[:32] + "...") if len(s.titulo) > 35 else s.titulo
            print(f"{s.id:<6} | {titulo_resumido:<35} | {s.categoria:<22} | {s.tempo_estimado_dias:>2} d  | {s.status}")

        aplicar = input("\nDeseja substituir a lista em memória pela versão ordenada? (s/N): ").strip().lower()
        if aplicar == "s":
            self.lista = lista_ordenada
            print(" [SUCESSO] Lista encadeada principal atualizada para a ordem classificada.")

    def op_analise_estatisticas(self):
        """Operação 8: Apresentar análise e estatísticas exigidas pelo edital."""
        self.limpar_tela_ou_separador()
        print("  >>> ANÁLISE DE DADOS E PROCESSAMENTO DAS ORIENTAÇÕES AO CIDADÃO <<<")
        print("=" * 75)

        stats = self.lista.gerar_estatisticas()
        total = stats["total_registros"]

        if total == 0:
            print(" [AVISO] Não há registros na lista encadeada para produzir relatórios.")
            return

        print(f" TOTAL GERAL DE SERVIÇOS CADASTRADOS: {total}")
        print(f" TEMPO MÉDIO ESTIMADO DE ATENDIMENTO:  {stats['tempo_medio_dias']} dias úteis\n")

        print(" DISTRIBUIÇÃO DE SERVIÇOS POR CATEGORIA:")
        print(f" {'CATEGORIA':<25} | {'QTD':<5} | {'PERCENTUAL':<12} | GRÁFICO")
        print(" " + "-" * 70)
        for cat, qtd in stats["por_categoria"].items():
            perc = stats["distribuicao_percentual"].get(cat, 0.0)
            barra = "#" * int(perc // 5)
            print(f" {cat:<25} | {qtd:<5} | {perc:>6.2f}%     | {barra}")

        print("\n DISTRIBUIÇÃO POR STATUS DO SERVIÇO:")
        for st, qtd in stats["por_status"].items():
            print(f"  * {st:<15}: {qtd} serviço(s)")

    def op_inspecionar_nos_dsa(self):
        """Operação 9: Visualizar explicitamente a topologia dos nós e ponteiros DSA."""
        self.limpar_tela_ou_separador()
        print("  >>> INSPEÇÃO EVIDENCIAL DA ESTRUTURA DE DADOS (NÓS & PONTEIROS) <<<")
        print("=" * 75)

        if self.lista.esta_vazia():
            print(" [AVISO] Lista encadeada vazia. Cabeça (head) -> NULL.")
            return

        nos = self.lista.inspecionar_ponteiros()
        print(f" Endereço da Cabeça (Head): {nos[0]['endereco_memoria_no']}\n")

        for no in nos:
            prox_repr = f"ID {no['proximo_id']:03d} ({no['endereco_memoria_prox']})" if no['proximo_id'] else "NULL (Fim da Lista)"
            print(f" [Nó #{no['indice']:02d}] Endereço: {no['endereco_memoria_no']}")
            print(f"   |-- Dado: ID {no['id']:03d} - {no['titulo']} ({no['categoria']})")
            print(f"   \\-- Ponteiro .proximo -> {prox_repr}")
            print("         |")
            print("         v")
        print("       [NULL]")

    def op_carregar_dados_iniciais(self):
        """Operação 10: Carga de dados iniciais a partir do arquivo JSON."""
        self.limpar_tela_ou_separador()
        print("  >>> CARGA DE REGISTROS DE DEMONSTRAÇÃO <<<")
        print("=" * 75)

        qtd = self.repositorio.carregar_para_lista(self.lista)
        print(f" [SUCESSO] Foram inseridos {qtd} novos registros na Lista Encadeada a partir do arquivo.")
        print(f" Total atual na lista: {self.lista.tamanho()} elementos.")

    def op_salvar_dados(self):
        """Operação 11: Persistência em disco."""
        self.limpar_tela_ou_separador()
        print("  >>> PERSISTÊNCIA DOS REGISTROS EM DISCO <<<")
        print("=" * 75)

        if self.repositorio.salvar_da_lista(self.lista):
            print(" [SUCESSO] Todos os registros da lista encadeada foram salvos no arquivo JSON.")
        else:
            print(" [ERRO] Não foi possível salvar os registros.")

    # ==========================================================================
    # LAÇO PRINCIPAL DO MENU
    # ==========================================================================

    def executar(self):
        """Executa o loop interativo do menu principal."""
        while True:
            self.limpar_tela_ou_separador()
            print("   ====================================================================")
            print("   *   GLOBAL SOLUTION 2026.2 | CITIZEN TECH - CITIZEN ASSIST AI    *")
            print("   *   Gerenciamento de Serviços Públicos com Estruturas de Dados   *")
            print("   *   Miguel Putini (571624) | Alexandre (569621) | Lucas (570029) *")
            print("   ====================================================================")
            print(f"   Status da Lista Encadeada: {self.lista.tamanho()} registro(s) armazenado(s)")
            print("   --------------------------------------------------------------------")
            print("   [1]  Cadastrar Novo Serviço Público (com ID único)")
            print("   [2]  Consultar Serviço por Identificador (Busca por ID)")
            print("   [3]  Pesquisar Serviços por Atributo (Título, Categoria, Geral)")
            print("   [4]  Listar Todos os Serviços (Percurso da Lista Encadeada)")
            print("   [5]  Atualizar Serviço Existente")
            print("   [6]  Excluir Serviço (Remoção e religação de nós)")
            print("   [7]  Ordenar Registros (Merge Sort / Insertion Sort / Selection Sort)")
            print("   [8]  Apresentar Análise e Estatísticas (Processamento dos Dados)")
            print("   [9]  Inspecionar Topologia de Nós e Ponteiros (Evidência DSA)")
            print("   [10] Carregar Dados Iniciais de Demonstração (Seed)")
            print("   [11] Salvar Alterações em Arquivo")
            print("   [0]  Encerrar o Sistema")
            print("   --------------------------------------------------------------------")

            opcao = self.ler_inteiro("   Selecione a operação desejada [0-11]: ", minimo=0, maximo=11)

            try:
                if opcao == 1:
                    self.op_cadastrar()
                elif opcao == 2:
                    self.op_consultar_por_id()
                elif opcao == 3:
                    self.op_pesquisar_atributo()
                elif opcao == 4:
                    self.op_listar_todos()
                elif opcao == 5:
                    self.op_atualizar()
                elif opcao == 6:
                    self.op_excluir()
                elif opcao == 7:
                    self.op_ordenar()
                elif opcao == 8:
                    self.op_analise_estatisticas()
                elif opcao == 9:
                    self.op_inspecionar_nos_dsa()
                elif opcao == 10:
                    self.op_carregar_dados_iniciais()
                elif opcao == 11:
                    self.op_salvar_dados()
                elif opcao == 0:
                    print("\n" + "=" * 75)
                    print(" Encerrando o sistema Citizen Assist AI. Até logo!")
                    print("=" * 75)
                    break
            except Exception as e:
                print(f"\n [ERRO INESPERADO NA OPERAÇÃO]: {e}")

            input("\nPressione [Enter] para retornar ao menu principal...")

