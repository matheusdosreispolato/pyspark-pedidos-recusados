import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder
        .appName("tests-relatorio-pedidos")
        .master("local[1]")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    yield session
    session.stop()
