import logging
from datetime import datetime

import pytest
from pyspark.sql.types import StringType, StructField, StructType

from business.relatorio_pedidos import RelatorioPedidosRecusados
from config.settings import AppConfig
from data_io.schemas import SchemaProvider


@pytest.fixture
def business():
    return RelatorioPedidosRecusados(AppConfig(ano_relatorio=2025))


@pytest.fixture
def pedidos(spark):
    dados = [
        ("p1", "NOTEBOOK", 1500.0, 2, datetime(2025, 3, 10, 8, 0), "SP", 1),
        ("p2", "TABLET", 1100.0, 1, datetime(2025, 1, 5, 9, 0), "SP", 2),
        ("p3", "MONITOR", 600.0, 3, datetime(2025, 2, 1, 10, 0), "RJ", 3),
        ("p4", "CELULAR", 1000.0, 1, datetime(2024, 12, 31, 23, 0), "SP", 4),
        ("p5", "SOUNDBAR", 900.0, 1, datetime(2025, 4, 2, 11, 0), "AC", 5),
        ("p6", "GELADEIRA", 2000.0, 1, datetime(2025, 5, 3, 12, 0), "BA", 6),
    ]
    return spark.createDataFrame(dados, SchemaProvider.pedidos())


@pytest.fixture
def pagamentos(spark):
    dados = [
        ("p1", "PIX", 3000.0, False, None, (False, 0.1)),
        ("p2", "BOLETO", 1100.0, False, None, (False, 0.2)),
        ("p3", "CARTAO_CREDITO", 1800.0, False, None, (False, 0.3)),
        ("p4", "PIX", 1000.0, False, None, (False, 0.1)),   # pedido de 2024
        ("p5", "PIX", 900.0, False, None, (True, 0.9)),     # fraude
        ("p6", "BOLETO", 2000.0, True, None, (False, 0.1)), # pagamento aprovado
    ]
    return spark.createDataFrame(dados, SchemaProvider.pagamentos())


def test_filtra_apenas_pedidos_do_ano(business, pedidos):
    resultado = business.filtrar_pedidos_ano(pedidos)
    assert {r.id_pedido for r in resultado.collect()} == {"p1", "p2", "p3", "p5", "p6"}


def test_calcula_valor_total(business, pedidos):
    resultado = {r.id_pedido: r.valor_total for r in business.calcular_valor_total(pedidos).collect()}
    assert resultado["p1"] == 3000.0
    assert resultado["p3"] == 1800.0


def test_filtra_pagamentos_recusados_e_legitimos(business, pagamentos):
    resultado = business.filtrar_pagamentos_recusados_legitimos(pagamentos)
    assert {r.id_pedido for r in resultado.collect()} == {"p1", "p2", "p3", "p4"}


def test_gera_relatorio_com_colunas_e_ordenacao(business, pedidos, pagamentos):
    resultado = business.gerar(pedidos, pagamentos)
    assert resultado.schema == SchemaProvider.relatorio()
    linhas = [(r.uf, r.forma_pagamento, r.id_pedido) for r in resultado.collect()]
    assert linhas == [
        ("RJ", "CARTAO_CREDITO", "p3"),
        ("SP", "BOLETO", "p2"),
        ("SP", "PIX", "p1"),
    ]


def test_registra_erro_no_log_e_relanca(business, spark, pagamentos, caplog):
    schema_invalido = StructType([StructField("id_pedido", StringType(), True)])
    pedidos_invalidos = spark.createDataFrame([("p1",)], schema_invalido)
    with caplog.at_level(logging.ERROR):
        with pytest.raises(Exception):
            business.gerar(pedidos_invalidos, pagamentos)
    assert "Erro ao gerar o relatório" in caplog.text
