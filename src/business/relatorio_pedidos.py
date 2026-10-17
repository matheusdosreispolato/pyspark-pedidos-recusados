import logging

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from config.settings import AppConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class RelatorioPedidosRecusados:
    """Regras de negócio do relatório de pedidos com pagamento recusado e avaliados como legítimos."""

    def __init__(self, config: AppConfig):
        self._config = config

    def filtrar_pedidos_ano(self, pedidos: DataFrame) -> DataFrame:
        logger.info("Filtrando pedidos do ano de %s", self._config.ano_relatorio)
        return pedidos.filter(F.year("data_criacao") == self._config.ano_relatorio)

    def calcular_valor_total(self, pedidos: DataFrame) -> DataFrame:
        logger.info("Calculando o valor total de cada pedido")
        return (
            pedidos
            .groupBy("id_pedido", "uf", "data_criacao")
            .agg(F.sum(F.col("valor_unitario") * F.col("quantidade")).cast("double").alias("valor_total"))
        )

    def filtrar_pagamentos_recusados_legitimos(self, pagamentos: DataFrame) -> DataFrame:
        logger.info("Filtrando pagamentos recusados (status=false) e legítimos (fraude=false)")
        return pagamentos.filter(
            (F.col("status") == F.lit(False))
            & (F.col("avaliacao_fraude.fraude") == F.lit(False))
        )

    def gerar(self, pedidos: DataFrame, pagamentos: DataFrame) -> DataFrame:
        try:
            logger.info("Iniciando geração do relatório")
            pedidos_ano = self.calcular_valor_total(self.filtrar_pedidos_ano(pedidos))
            pagamentos_filtrados = self.filtrar_pagamentos_recusados_legitimos(pagamentos)

            logger.info("Cruzando pedidos e pagamentos pelo id_pedido")
            relatorio = (
                pedidos_ano.join(pagamentos_filtrados, on="id_pedido", how="inner")
                .select(
                    F.col("id_pedido"),
                    F.col("uf"),
                    F.col("forma_pagamento"),
                    F.col("valor_total"),
                    F.col("data_criacao").alias("data_pedido"),
                )
                .orderBy("uf", "forma_pagamento", "data_pedido")
            )
            logger.info("Relatório gerado com %d registros", relatorio.count())
            return relatorio
        except Exception as erro:
            logger.error("Erro ao gerar o relatório: %s", erro, exc_info=True)
            raise
