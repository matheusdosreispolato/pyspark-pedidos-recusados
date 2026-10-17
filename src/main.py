from business.relatorio_pedidos import RelatorioPedidosRecusados
from config.settings import AppConfig
from data_io.readers import PagamentosReader, PedidosReader
from data_io.schemas import SchemaProvider
from data_io.writers import ParquetWriter
from pipeline.relatorio_pipeline import RelatorioPipeline
from session.spark_session_manager import SparkSessionManager


def main() -> None:
    """Aggregation root: instancia todas as dependências e as injeta no pipeline."""
    config = AppConfig.from_env()
    session_manager = SparkSessionManager(config)
    spark = session_manager.get_session()
    schemas = SchemaProvider()

    pipeline = RelatorioPipeline(
        pedidos_reader=PedidosReader(spark, schemas.pedidos(), config),
        pagamentos_reader=PagamentosReader(spark, schemas.pagamentos(), config),
        business=RelatorioPedidosRecusados(config),
        writer=ParquetWriter(config),
    )

    try:
        pipeline.executar()
    finally:
        session_manager.stop()


if __name__ == "__main__":
    main()
