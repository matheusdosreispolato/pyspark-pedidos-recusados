from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

from config.settings import AppConfig


class PedidosReader:
    """Lê o dataset de pedidos (CSV gzip, separador ';')."""

    def __init__(self, spark: SparkSession, schema: StructType, config: AppConfig):
        self._spark = spark
        self._schema = schema
        self._config = config

    def read(self) -> DataFrame:
        return (
            self._spark.read
            .schema(self._schema)
            .option("header", True)
            .option("sep", self._config.csv_separator)
            .option("timestampFormat", self._config.pedidos_timestamp_format)
            .csv(self._config.pedidos_path)
        )


class PagamentosReader:
    """Lê o dataset de pagamentos (JSON lines gzip)."""

    def __init__(self, spark: SparkSession, schema: StructType, config: AppConfig):
        self._spark = spark
        self._schema = schema
        self._config = config

    def read(self) -> DataFrame:
        return (
            self._spark.read
            .schema(self._schema)
            .option("timestampFormat", self._config.pagamentos_timestamp_format)
            .json(self._config.pagamentos_path)
        )
