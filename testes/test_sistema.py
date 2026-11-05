"""
Suíte de Testes Automatizados para o Citizen Assist AI.
Global Solution 2026.2 - Data Structures and Algorithms (DSA).
Cobre casos normais, casos de borda, entradas inválidas e operações com lista vazia.
"""

import unittest
from src.modelos.servico import ServicoPublico
from src.estruturas.no import Node
from src.estruturas.lista_encadeada import ListaEncadeada
from src.algoritmos.busca import busca_linear_id, busca_linear_atributo, busca_binaria_em_vetor
from src.algoritmos.ordenacao import merge_sort_lista, insertion_sort_lista, selection_sort_lista


class TestServicoPublico(unittest.TestCase):
    """Testes de integridade do modelo de dados."""

    def test_criacao_valida(self):
        s = ServicoPublico(
            id_servico=1,
            titulo="Consulta Médica",
            categoria="Saúde",
            descricao="Atendimento clínico geral",
            requisitos="Cartão SUS",
            local_atendimento="UBS Central",
            publico_alvo="Munícipes",
            tempo_estimado_dias=2,
            status="Ativo"
        )
        self.assertEqual(s.id, 1)
        self.assertEqual(s.titulo, "Consulta Médica")
        self.assertEqual(s.categoria, "Saúde")

    def test_id_invalido_rejeicao(self):
        # ID negativo
        with self.assertRaises(ValueError):
            ServicoPublico(id_servico=-5, titulo="X", categoria="Saúde", descricao="D", requisitos="R", local_atendimento="L")

        # ID zero
        with self.assertRaises(ValueError):
            ServicoPublico(id_servico=0, titulo="X", categoria="Saúde", descricao="D", requisitos="R", local_atendimento="L")

        # ID string não numérica
        with self.assertRaises(ValueError):
            ServicoPublico(id_servico="abc", titulo="X", categoria="Saúde", descricao="D", requisitos="R", local_atendimento="L")

    def test_campos_obrigatorios_vazios(self):
        with self.assertRaises(ValueError):
            ServicoPublico(id_servico=1, titulo="   ", categoria="Saúde", descricao="D", requisitos="R", local_atendimento="L")

        with self.assertRaises(ValueError):
            ServicoPublico(id_servico=1, titulo="Ok", categoria="Saúde", descricao="", requisitos="R", local_atendimento="L")


class TestListaEncadeada(unittest.TestCase):
    """Testes formais da estrutura de dados Lista Simplesmente Encadeada."""

    def setUp(self):
        self.lista = ListaEncadeada()
        self.s1 = ServicoPublico(10, "Vacinação", "Saúde", "D", "R", "L", tempo_estimado_dias=1)
        self.s2 = ServicoPublico(20, "RG", "Documentação e Cidadania", "D", "R", "L", tempo_estimado_dias=5)
        self.s3 = ServicoPublico(30, "CadÚnico", "Assistência Social", "D", "R", "L", tempo_estimado_dias=10)

    def test_lista_inicialmente_vazia(self):
        self.assertTrue(self.lista.esta_vazia())
        self.assertEqual(self.lista.tamanho(), 0)
        self.assertIsNone(self.lista.cabeca)

    def test_insercao_inicio_e_fim(self):
        self.lista.inserir_fim(self.s2)  # [20]
        self.lista.inserir_inicio(self.s1)  # [10 -> 20]
        self.lista.inserir_fim(self.s3)  # [10 -> 20 -> 30]

        self.assertEqual(self.lista.tamanho(), 3)
        self.assertEqual(self.lista.cabeca.dado.id, 10)
        self.assertEqual(self.lista.cabeca.proximo.dado.id, 20)
        self.assertEqual(self.lista.cabeca.proximo.proximo.dado.id, 30)
        self.assertIsNone(self.lista.cabeca.proximo.proximo.proximo)

    def test_rejeicao_id_duplicado(self):
        self.lista.inserir_fim(self.s1)
        duplicado = ServicoPublico(10, "Outro", "Saúde", "D", "R", "L")
        with self.assertRaises(ValueError):
            self.lista.inserir_fim(duplicado)
        with self.assertRaises(ValueError):
            self.lista.inserir_inicio(duplicado)

    def test_remocao_cabeca_meio_fim(self):
        self.lista.inserir_fim(self.s1)  # 10
        self.lista.inserir_fim(self.s2)  # 20
        self.lista.inserir_fim(self.s3)  # 30

        # Remover meio (20)
        removido_meio = self.lista.remover_por_id(20)
        self.assertEqual(removido_meio.id, 20)
        self.assertEqual(self.lista.tamanho(), 2)
        self.assertEqual(self.lista.cabeca.proximo.dado.id, 30)

        # Remover cabeça (10)
        removido_cabeca = self.lista.remover_por_id(10)
        self.assertEqual(removido_cabeca.id, 10)
        self.assertEqual(self.lista.tamanho(), 1)
        self.assertEqual(self.lista.cabeca.dado.id, 30)

        # Remover cauda / único elemento (30)
        removido_cauda = self.lista.remover_por_id(30)
        self.assertEqual(removido_cauda.id, 30)
        self.assertTrue(self.lista.esta_vazia())
        self.assertIsNone(self.lista.cabeca)

    def test_operacoes_em_lista_vazia(self):
        # Remover em lista vazia não deve lançar exceção
        self.assertIsNone(self.lista.remover_por_id(999))
        self.assertIsNone(self.lista.buscar_por_id(999))
        stats = self.lista.gerar_estatisticas()
        self.assertEqual(stats["total_registros"], 0)


class TestAlgoritmosBusca(unittest.TestCase):
    """Testes dos algoritmos de busca e casos sem resultado."""

    def setUp(self):
        self.lista = ListaEncadeada()
        self.s1 = ServicoPublico(101, "Agendamento UBS", "Saúde", "Consulta", "Doc", "Posto")
        self.s2 = ServicoPublico(102, "Vacina Dengue", "Saúde", "Dose", "Doc", "Posto")
        self.s3 = ServicoPublico(103, "Emissão CIN RG", "Documentação e Cidadania", "Identidade", "Certidao", "Poupatempo")
        self.lista.inserir_fim(self.s1)
        self.lista.inserir_fim(self.s2)
        self.lista.inserir_fim(self.s3)

    def test_busca_linear_id_existente(self):
        servico, metricas = busca_linear_id(self.lista, 102)
        self.assertIsNotNone(servico)
        self.assertEqual(servico.id, 102)
        self.assertTrue(metricas["encontrado"])
        self.assertEqual(metricas["comparacoes"], 2)

    def test_busca_linear_id_inexistente(self):
        servico, metricas = busca_linear_id(self.lista, 999)
        self.assertIsNone(servico)
        self.assertFalse(metricas["encontrado"])
        self.assertEqual(metricas["comparacoes"], 3)  # Percorreu todos os 3 nós

    def test_busca_linear_atributo_titulo_e_categoria(self):
        # Busca por categoria 'Saúde' (2 resultados)
        res, m = busca_linear_atributo(self.lista, "categoria", "Saúde")
        self.assertEqual(len(res), 2)
        self.assertTrue(m["encontrado"])

        # Busca por substring no título
        res_tit, m_tit = busca_linear_atributo(self.lista, "titulo", "vacina")
        self.assertEqual(len(res_tit), 1)
        self.assertEqual(res_tit[0].id, 102)

        # Busca sem correspondência
        res_vazia, m_vazia = busca_linear_atributo(self.lista, "titulo", "InexistenteXYZ")
        self.assertEqual(len(res_vazia), 0)
        self.assertFalse(m_vazia["encontrado"])

    def test_busca_binaria_vetor_ordenado(self):
        vetor = [self.s1, self.s2, self.s3]  # ordenados por ID: 101, 102, 103
        item, m = busca_binaria_em_vetor(vetor, 103)
        self.assertIsNotNone(item)
        self.assertEqual(item.id, 103)
        self.assertTrue(m["encontrado"])

        item_inex, m_inex = busca_binaria_em_vetor(vetor, 999)
        self.assertIsNone(item_inex)
        self.assertFalse(m_inex["encontrado"])


class TestAlgoritmosOrdenacao(unittest.TestCase):
    """Testes dos algoritmos de ordenação implementados do zero."""

    def setUp(self):
        self.lista = ListaEncadeada()
        # Inserção fora de ordem
        self.lista.inserir_fim(ServicoPublico(300, "Zoológico Municipal", "Educação e Qualificação", "D", "R", "L", tempo_estimado_dias=10))
        self.lista.inserir_fim(ServicoPublico(100, "Acolhimento Social", "Assistência Social", "D", "R", "L", tempo_estimado_dias=2))
        self.lista.inserir_fim(ServicoPublico(200, "Médico de Família", "Saúde", "D", "R", "L", tempo_estimado_dias=5))

    def test_merge_sort_por_id_crescente(self):
        ordenada, m = merge_sort_lista(self.lista, criterio="id", asc=True)
        ids = [s.id for s in ordenada]
        self.assertEqual(ids, [100, 200, 300])
        self.assertGreater(m["comparacoes"], 0)

    def test_merge_sort_por_id_decrescente(self):
        ordenada, m = merge_sort_lista(self.lista, criterio="id", asc=False)
        ids = [s.id for s in ordenada]
        self.assertEqual(ids, [300, 200, 100])

    def test_merge_sort_por_titulo(self):
        ordenada, m = merge_sort_lista(self.lista, criterio="titulo", asc=True)
        titulos = [s.titulo for s in ordenada]
        self.assertEqual(titulos, ["Acolhimento Social", "Médico de Família", "Zoológico Municipal"])

    def test_insertion_sort_por_id(self):
        ordenada, m = insertion_sort_lista(self.lista, criterio="id", asc=True)
        ids = [s.id for s in ordenada]
        self.assertEqual(ids, [100, 200, 300])

    def test_selection_sort_por_prazo(self):
        ordenada, m = selection_sort_lista(self.lista, criterio="prazo", asc=True)
        prazos = [s.tempo_estimado_dias for s in ordenada]
        self.assertEqual(prazos, [2, 5, 10])

    def test_ordenacao_lista_vazia(self):
        lista_vazia = ListaEncadeada()
        ord_merge, m1 = merge_sort_lista(lista_vazia)
        ord_ins, m2 = insertion_sort_lista(lista_vazia)
        self.assertTrue(ord_merge.esta_vazia())
        self.assertTrue(ord_ins.esta_vazia())


if __name__ == "__main__":
    unittest.main()

