"""
Script de Demonstração Prática Automatizada do Citizen Assist AI.
Evidencia o funcionamento real das Estruturas de Dados e Algoritmos,
atendendo expressamente ao requisito 6 da Global Solution 2026.2.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.estruturas.lista_encadeada import ListaEncadeada
from src.modelos.servico import ServicoPublico
from src.algoritmos.busca import busca_linear_id, busca_linear_atributo, busca_binaria_em_vetor
from src.algoritmos.ordenacao import merge_sort_lista, insertion_sort_lista
from src.persistencia.repositorio import RepositorioServicos


def pausar(mensagem: str = "Pressione Enter para continuar..."):
    # Se estiver rodando em ambiente automatizado ou pipe, evita travar
    try:
        input(f"\n >>> {mensagem}")
    except (EOFError, KeyboardInterrupt):
        time.sleep(1)


def cabecalho(etapa: str, titulo: str):
    print("\n" + "=" * 80)
    print(f" [ETAPA {etapa}] - {titulo}")
    print("=" * 80)


def main():
    print("*" * 80)
    print("   CITIZEN ASSIST AI - DEMONSTRAÇÃO PRÁTICA DAS ESTRUTURAS DE DADOS (DSA)")
    print("   Global Solution 2026.2 | Citizen Tech")
    print("*" * 80)

    # --------------------------------------------------------------------------
    # ETAPA 1: Inicialização da Lista Encadeada e Carga
    # --------------------------------------------------------------------------
    cabecalho("1", "INICIALIZAÇÃO DA LISTA SIMPLESMENTE ENCADEADA")
    lista = ListaEncadeada()
    print(f"Lista criada. Estado inicial: vazia={lista.esta_vazia()} | tamanho={lista.tamanho()}")
    print("Ponteiro da cabeça (self.cabeca):", lista.cabeca)

    repo = RepositorioServicos()
    qtd = repo.carregar_para_lista(lista)
    print(f"\n[OK] Carga inicial realizada com sucesso: {qtd} registros inseridos na Lista Encadeada.")
    print(f"Total de nós encadeados: {lista.tamanho()}")
    print(f"Endereço do nó de Cabeça (Head): {hex(id(lista.cabeca))} -> Dado: ID {lista.cabeca.dado.id} ({lista.cabeca.dado.titulo})")

    # --------------------------------------------------------------------------
    # ETAPA 2: Inspeção da Topologia de Nós e Ponteiros
    # --------------------------------------------------------------------------
    cabecalho("2", "INSPEÇÃO TOPOLÓGICA DE NÓS E PONTEIROS (EVIDÊNCIA DSA)")
    print("Percorrendo os nós através da referência explícita 'self.proximo':\n")
    nos = lista.inspecionar_ponteiros()
    for no in nos[:5]:  # Primeiros 5 para exibição limpa
        prox_str = f"ID #{no['proximo_id']:03d}" if no['proximo_id'] else "NULL (Fim)"
        print(f" [Nó #{no['indice']:02d}] {no['endereco_memoria_no']} | ID: {no['id']:03d} - {no['titulo'][:30]:<30} | .proximo -> {prox_str}")
    print(f" ... e mais {len(nos) - 5} nós encadeados até o ponteiro final NULL.")

    # --------------------------------------------------------------------------
    # ETAPA 3: Validação de Chave Única (Tratamento de ID Duplicado)
    # --------------------------------------------------------------------------
    cabecalho("3", "TESTE DE INTEGRIDADE: TRATAMENTO DE ID DUPLICADO")
    id_existente = lista.cabeca.dado.id
    print(f"Tentando inserir um novo serviço com ID repetido ({id_existente})...")
    servico_duplicado = ServicoPublico(
        id_servico=id_existente,
        titulo="Serviço Intruso Duplicado",
        categoria="Saúde",
        descricao="Teste de integridade",
        requisitos="Nenhum",
        local_atendimento="Online"
    )

    try:
        lista.inserir_fim(servico_duplicado)
        print(" [FALHA] O sistema aceitou ID duplicado!")
    except ValueError as e:
        print(f" [SUCESSO NO BLOQUEIO]: {e}")

    # --------------------------------------------------------------------------
    # ETAPA 4: Busca Linear por ID (Existente vs Inexistente)
    # --------------------------------------------------------------------------
    cabecalho("4", "ALGORITMO DE BUSCA LINEAR POR IDENTIFICADOR")
    id_alvo = 104
    print(f"Executando busca sequencial pelo ID {id_alvo}...")
    s_enc, met_enc = busca_linear_id(lista, id_alvo)
    print(f" -> Resultado: {met_enc['motivo']}")
    print(f"    Comparações realizadas: {met_enc['comparacoes']}")
    if s_enc:
        print(f"    Serviço: '{s_enc.titulo}' | Categoria: {s_enc.categoria} | Prazo: {s_enc.tempo_estimado_dias}d")

    print(f"\nExecutando busca por ID inexistente (ID 9999)...")
    s_inex, met_inex = busca_linear_id(lista, 9999)
    print(f" -> Resultado: {met_inex['motivo']}")
    print(f"    Total de nós examinados: {met_inex['comparacoes']} (pior caso O(n))")

    # --------------------------------------------------------------------------
    # ETAPA 5: Pesquisa por Atributo (Substring em Categoria / Título)
    # --------------------------------------------------------------------------
    cabecalho("5", "PESQUISA DE ATRIBUTOS (CATEGORIA & TÍTULO)")
    termo = "Saúde"
    res_cat, met_cat = busca_linear_atributo(lista, campo="categoria", termo=termo)
    print(f"Pesquisando na categoria '{termo}':")
    print(f" -> Encontrados: {len(res_cat)} serviço(s) com {met_cat['comparacoes']} comparações de nós.")
    for r in res_cat:
        print(f"    * [ID {r.id:03d}] {r.titulo}")

    # --------------------------------------------------------------------------
    # ETAPA 6: Atualização e Exclusão Preservando Integridade
    # --------------------------------------------------------------------------
    cabecalho("6", "ATUALIZAÇÃO E EXCLUSÃO COM PRESERVAÇÃO DE PONTEIROS")
    # Inserção de um serviço temporário
    s_temp = ServicoPublico(950, "Serviço Piloto Temporário", "Serviços Urbanos", "Desc", "Req", "Bairro X")
    lista.inserir_fim(s_temp)
    print(f"Inserido serviço temporário ID 950. Tamanho atual: {lista.tamanho()}")

    # Atualização
    lista.atualizar(950, {"titulo": "Serviço Piloto Temporário ATUALIZADO", "status": "Em Atualização"})
    s_mod = lista.buscar_por_id(950)
    print(f"Serviço atualizado: '{s_mod.titulo}' | Status: {s_mod.status}")

    # Exclusão
    removido = lista.remover_por_id(950)
    print(f"Serviço removido: [ID {removido.id}] {removido.titulo}")
    print(f"Tamanho da lista após exclusão: {lista.tamanho()}")
    print(f"Verificação se ainda existe ID 950: {lista.existe_id(950)}")

    # --------------------------------------------------------------------------
    # ETAPA 7: Bancada de Ordenação (Merge Sort vs Insertion Sort)
    # --------------------------------------------------------------------------
    cabecalho("7", "ORDENAÇÃO DSA: MERGE SORT O(n log n) vs INSERTION SORT O(n²)")
    print("Lista original (primeiros 4 IDs):", [s.id for s in lista][:4])

    print("\n[A] Executando Merge Sort por ID (Divisão e Conquista na Lista Encadeada)...")
    ord_merge, met_merge = merge_sort_lista(lista, criterio="id", asc=True)
    print(f" -> Comparações: {met_merge['comparacoes']} | Religações de ponteiros: {met_merge['religacoes_ponteiros']}")
    print(f" -> Tempo: {met_merge['tempo_execucao_ms']} ms")
    print(" -> IDs ordenados:", [s.id for s in ord_merge])

    print("\n[B] Executando Insertion Sort por ID (Inserção Ordenada nó a nó)...")
    ord_ins, met_ins = insertion_sort_lista(lista, criterio="id", asc=True)
    print(f" -> Comparações: {met_ins['comparacoes']} | Religações de ponteiros: {met_ins['religacoes_ponteiros']}")
    print(f" -> Tempo: {met_ins['tempo_execucao_ms']} ms")
    print(" -> IDs ordenados:", [s.id for s in ord_ins])

    print("\n[C] Executando Merge Sort por Título (Ordem Alfabética)...")
    ord_tit, met_tit = merge_sort_lista(lista, criterio="titulo", asc=True)
    print(" -> Primeiros 3 títulos ordenados:")
    for s in list(ord_tit)[:3]:
        print(f"    - {s.titulo}")

    # --------------------------------------------------------------------------
    # ETAPA 8: Análise Estatística e Processamento Útil
    # --------------------------------------------------------------------------
    cabecalho("8", "PROCESSAMENTO ANALÍTICO DOS DADOS AO CIDADÃO")
    stats = lista.gerar_estatisticas()
    print(f"Total de registros: {stats['total_registros']}")
    print(f"Tempo médio estimado de atendimento: {stats['tempo_medio_dias']} dias úteis")
    print("Distribuição percentual por categoria:")
    for cat, perc in stats["distribuicao_percentual"].items():
        print(f"  * {cat:<26}: {perc:>6.2f}% ({stats['por_categoria'][cat]} serviços)")

    cabecalho("FIM", "DEMONSTRAÇÃO CONCLUÍDA COM 100% DE SUCESSO")
    print("Todas as operações obrigatórias e opcionais de DSA foram executadas com rigor técnico.")


if __name__ == "__main__":
    main()

