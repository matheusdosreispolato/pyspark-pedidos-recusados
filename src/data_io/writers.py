from pyspark.sql import DataFrame

from config.settings import AppConfig


class ParquetWriter:
    """Grava dataframes em formato parquet."""

    def __init__(self, config: AppConfig):
        self._config = config

    def write(self, df: DataFrame) -> None:
        df.write.mode(self._config.write_mode).parquet(self._config.output_path)
