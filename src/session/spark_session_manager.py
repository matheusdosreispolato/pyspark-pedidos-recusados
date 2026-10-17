from typing import Optional

from pyspark.sql import SparkSession

from config.settings import AppConfig


class SparkSessionManager:
    """Gerencia o ciclo de vida da SparkSession."""

    def __init__(self, config: AppConfig):
        self._config = config
        self._spark: Optional[SparkSession] = None

    def get_session(self) -> SparkSession:
        if self._spark is None:
            self._spark = (
                SparkSession.builder
                .appName(self._config.app_name)
                .master(self._config.spark_master)
                .config("spark.sql.session.timeZone", "UTC")
                .config("spark.ui.showConsoleProgress", "false")
                .getOrCreate()
            )
            self._spark.sparkContext.setLogLevel("WARN")
        return self._spark

    def stop(self) -> None:
        if self._spark is not None:
            self._spark.stop()
            self._spark = None
