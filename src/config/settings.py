import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Configurações centralizadas da aplicação."""

    app_name: str = "relatorio-pedidos-recusados"
    spark_master: str = "local[*]"
    pedidos_path: str = "data/input/datasets-csv-pedidos/data/pedidos/"
    pagamentos_path: str = "data/input/dataset-json-pagamentos/data/pagamentos/"
    output_path: str = "data/output/relatorio_pedidos_recusados"
    ano_relatorio: int = 2025
    csv_separator: str = ";"
    pedidos_timestamp_format: str = "yyyy-MM-dd'T'HH:mm:ss"
    pagamentos_timestamp_format: str = "yyyy-MM-dd'T'HH:mm:ss[.SSSSSS]"
    write_mode: str = "overwrite"

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Cria a configuração permitindo sobrescrever valores por variáveis de ambiente."""
        default = cls()
        return cls(
            app_name=os.getenv("APP_NAME", default.app_name),
            spark_master=os.getenv("SPARK_MASTER", default.spark_master),
            pedidos_path=os.getenv("PEDIDOS_PATH", default.pedidos_path),
            pagamentos_path=os.getenv("PAGAMENTOS_PATH", default.pagamentos_path),
            output_path=os.getenv("OUTPUT_PATH", default.output_path),
            ano_relatorio=int(os.getenv("ANO_RELATORIO", default.ano_relatorio)),
        )
