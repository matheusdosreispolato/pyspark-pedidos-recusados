from pyspark.sql.types import (
    BooleanType,
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


class SchemaProvider:
    """Schemas explícitos de todos os dataframes do projeto (sem inferência)."""

    @staticmethod
    def pedidos() -> StructType:
        return StructType([
            StructField("id_pedido", StringType(), True),
            StructField("produto", StringType(), True),
            StructField("valor_unitario", DoubleType(), True),
            StructField("quantidade", LongType(), True),
            StructField("data_criacao", TimestampType(), True),
            StructField("uf", StringType(), True),
            StructField("id_cliente", LongType(), True),
        ])

    @staticmethod
    def pagamentos() -> StructType:
        return StructType([
            StructField("id_pedido", StringType(), True),
            StructField("forma_pagamento", StringType(), True),
            StructField("valor_pagamento", DoubleType(), True),
            StructField("status", BooleanType(), True),
            StructField("data_processamento", TimestampType(), True),
            StructField("avaliacao_fraude", StructType([
                StructField("fraude", BooleanType(), True),
                StructField("score", DoubleType(), True),
            ]), True),
        ])

    @staticmethod
    def relatorio() -> StructType:
        return StructType([
            StructField("id_pedido", StringType(), True),
            StructField("uf", StringType(), True),
            StructField("forma_pagamento", StringType(), True),
            StructField("valor_total", DoubleType(), True),
            StructField("data_pedido", TimestampType(), True),
        ])
