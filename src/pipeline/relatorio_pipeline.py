import logging

from business.relatorio_pedidos import RelatorioPedidosRecusados
from data_io.readers import PagamentosReader, PedidosReader
from data_io.writers import ParquetWriter

logger = logging.getLogger(__name__)


class RelatorioPipeline:
    """Orquestra o pipeline: leitura -> regras de negócio -> escrita."""

    def __init__(
        self,
        pedidos_reader: PedidosReader,
        pagamentos_reader: PagamentosReader,
        business: RelatorioPedidosRecusados,
        writer: ParquetWriter,
    ):
        self._pedidos_reader = pedidos_reader
        self._pagamentos_reader = pagamentos_reader
        self._business = business
        self._writer = writer

    def executar(self) -> None:
        logger.info("Pipeline iniciado: lendo datasets de pedidos e pagamentos")
        pedidos = self._pedidos_reader.read()
        pagamentos = self._pagamentos_reader.read()

        relatorio = self._business.gerar(pedidos, pagamentos)
        relatorio.show(10, truncate=False)

        logger.info("Gravando relatório em parquet")
        self._writer.write(relatorio)
        logger.info("Pipeline finalizado com sucesso")
