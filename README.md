# Relatório de Pedidos Recusados e Legítimos – PySpark

Trabalho final da disciplina **Data Engineering Programming** (FIAP – Prof. Marcelo Barbosa Pinto).

## Objetivo

Gerar, em **parquet**, o relatório de pedidos de venda de **2025** cujo pagamento foi **recusado** (`status = false`) e que na avaliação de fraude foram classificados como **legítimos** (`avaliacao_fraude.fraude = false`).

| Coluna            | Descrição                                   |
|-------------------|---------------------------------------------|
| `id_pedido`       | Identificador do pedido                     |
| `uf`              | Estado (UF) onde o pedido foi feito         |
| `forma_pagamento` | Forma de pagamento                          |
| `valor_total`     | Valor total do pedido (`valor_unitario * quantidade`) |
| `data_pedido`     | Data de criação do pedido                   |

O relatório sai ordenado por `uf`, `forma_pagamento` e `data_pedido`.

## Datasets

- Pedidos: <https://github.com/infobarbosa/datasets-csv-pedidos> (`data/pedidos/`, CSV gzip, separador `;`)
- Pagamentos: <https://github.com/infobarbosa/dataset-json-pagamentos> (`data/pagamentos/`, JSON lines gzip)

O script `scripts/download_datasets.sh` clona os dois repositórios em `data/input/`.

## Estrutura do projeto

```
├── src/
│   ├── main.py                          # Aggregation root (instancia e injeta as dependências)
│   ├── config/settings.py               # AppConfig: configurações centralizadas
│   ├── session/spark_session_manager.py # SparkSessionManager: ciclo de vida da SparkSession
│   ├── data_io/schemas.py               # SchemaProvider: schemas explícitos
│   ├── data_io/readers.py               # PedidosReader / PagamentosReader
│   ├── data_io/writers.py               # ParquetWriter
│   ├── business/relatorio_pedidos.py    # RelatorioPedidosRecusados: regras de negócio + logging + try/except
│   └── pipeline/relatorio_pipeline.py   # RelatorioPipeline: orquestração
├── tests/                               # Testes unitários (pytest)
├── scripts/download_datasets.sh
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

## Execução com Docker (recomendado, funciona em Linux, macOS e Windows)

Pré-requisito: Docker. Execute os comandos a partir da raiz do repositório.

```bash
docker build -t pedidos-recusados .
docker run --rm -v "$(pwd)":/app pedidos-recusados bash scripts/download_datasets.sh
docker run --rm -v "$(pwd)":/app pedidos-recusados pytest -v
docker run --rm -v "$(pwd)":/app pedidos-recusados python src/main.py
```

> No Windows PowerShell, troque `"$(pwd)"` por `"${PWD}"`.

## Execução local (sem Docker)

Pré-requisitos: Python 3.9 a 3.12, Java 17 (`JAVA_HOME` configurado), `git` e `bash`.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
bash scripts/download_datasets.sh
pytest -v
python src/main.py
```

Como alternativa, `pip install -e ".[dev]"` instala o projeto e cria o comando `relatorio-pedidos`.

> No Windows nativo, a gravação em parquet pelo Spark exige o `winutils.exe` do Hadoop. Por isso o Docker é o caminho recomendado.

## Configuração

Os valores padrão ficam em `src/config/settings.py` e podem ser sobrescritos por variáveis de ambiente:

| Variável          | Padrão |
|-------------------|--------|
| `PEDIDOS_PATH`    | `data/input/datasets-csv-pedidos/data/pedidos/` |
| `PAGAMENTOS_PATH` | `data/input/dataset-json-pagamentos/data/pagamentos/` |
| `OUTPUT_PATH`     | `data/output/relatorio_pedidos_recusados` |
| `ANO_RELATORIO`   | `2025` |
| `SPARK_MASTER`    | `local[*]` |

## Saída

O relatório é gravado em `data/output/relatorio_pedidos_recusados/` (parquet). Com os datasets atuais, ele tem **1.473 pedidos**.

## Testes

`tests/test_relatorio_pedidos.py` cobre a classe de lógica de negócio:

- o filtro por ano;
- o cálculo do valor total;
- o filtro de pagamentos recusados e legítimos;
- as colunas e a ordenação do relatório;
- o registro do erro em log, com a exceção relançada.
