# 📊 Crypto Explorer
> **End-to-end data engineering pipeline + interactive analytics layer**

Este repositório demonstra domínio prático de Engenharia de Dados, cobrindo as etapas — ingestão, modelagem, persistência, orquestração e visualização — em um contexto de mercado cripto. O pipeline coleta ativos e histórico de preços diretamente da **API CoinCap**, grava em banco relacional e disponibiliza via Streamlit para análise exploratória.

---

## 🚀 Demo ao vivo

👉 **Clique aqui para acessar o Streamlit:** [![Abrir no Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://leandroavidigal-projetocadastra.streamlit.app/)

*(O deploy usa Streamlit Cloud; basta clicar e testar.)*

---

## 📐 Arquitetura


                                      ┌───────────────────────┐
                                      │      CoinCap API      │
                                      │   (resposta em JSON)  │
                                      └────────────┬──────────┘
                                                   │
                                        requests + tratamento JSON
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │   api_client.py        │
                                      │ → fetch_assets()       │
                                      │ → fetch_asset_history()│
                                      └────────────┬───────────┘
                                                   │
                                        Dados em formato dict/list
                                                   ▼
                                   ┌────────────────────────────────┐
                                   │ Conversão parapandas.DataFrame │
                                   │ (transformações, limpeza)      │
                                   └───────────────┬────────────────┘
                                                   │
                                                   ▼
                                         ┌─────────────────────┐
                                         │     ORM Layer       │
                                         │     (models.py)     │
                                         └────────┬────────────┘
                                                  │
                                 SQLAlchemy → mapeamento relacional
                                                  │
                                                  ▼
                                       ┌────────────────────────┐
                                       │ Banco de Dados (SQLite)│
                                       │  → crypto.db           │
                                       │  → assets / history    │
                                       └──────────┬─────────────┘
                                                  │
                                     Leitura com pandas + SQLAlchemy
                                                  │
                                                  ▼
                                      ┌────────────────────────┐
                                      │     app.py (Streamlit) │
                                      │ → ranking, gráficos    │
                                      │ → filtros e exportação │
                                      └────────────────────────┘


---

## 🎯 Metas Técnicas (atendidas)

- **Python 3.10 + PEP 8 clean code** com separação de responsabilidades por módulo  
- **Ingestão resiliente**: paginação, back-off e tratamento de HTTP 403; ativos problemáticos registrados em CSV  
- **Modelagem relacional 2NF** (`assets`, `asset_history`) com chave estrangeira e unicidade temporal  
- **Persistência**: bulk-upsert idempotente, transação segura, sessão reutilizável  
- **Configuração externa** via `.env` (API key, URL do DB, page size)  
- **Dashboard analítico** em Streamlit com ranking, séries temporais, export CSV  
- **Pronto para CI/CD**: requirements, script único de bootstrap e deploy simples no Streamlit Cloud

---

## 🗂️ Estrutura do repositório

| Caminho / Arquivo | Responsabilidade |
|-------------------|------------------|
| `app.py` | UI Streamlit (dashboard) |
| `main.py` | Orquestração da ingestão end-to-end |
| `api_client.py` | Wrapper CoinCap REST (retry & auth) |
| `models.py` | ORM SQLAlchemy (`Asset`, `AssetHistory`) |
| `db.py` | Engine, session factory |
| `utils.py` | Funções auxiliares para queries e métricas |
| `scriptsinit_db.sql` | DDL equivalente (referência) |
| `.env.example` | Template de variáveis sensíveis |
| `requirements.txt` | Lock mínimo de dependências |
| `crypto.db` | **(opcional)** dump SQLite pequeno para testes |
| `README.md` | Documentação completa |

---

## ⚙️ Execução local

#### 1. Clonar
git clone https://github.com/SEU_USUARIO/crypto-explorer.git
cd crypto-explorer

#### 2. Variáveis de ambiente
cp .env.example .env #### edite COINCAP_API_KEY e DB_URL

#### 3. Dependências
pip install -r requirements.txt

#### 4. Ingestão (cria/atualiza banco)
python main.py

#### 5. Dashboard
streamlit run app.py

---

## 📈 Funcionalidades analíticas

| Recurso                          | Descrição                                                    |
| -------------------------------- | ------------------------------------------------------------ |
| **Ranking Top-N**                | Ordenação dinâmica por market cap, preço ou volume           |
| **Time Series**                  | Linha temporal de preço e volume com zoom e seleção de datas |
| **Export CSV**                   | Baixe o histórico filtrado para uso em BI/ML                 |
| **Filtro de ativos**             | Combobox rápido alimentado pelo banco                        |
| **Relatório de inconsistências** | `ativos_sem_historico.csv` com slugs que retornaram HTTP 403 |

---

## 🔄 Extensões futuras (road-map)

* Scheduler (Airflow/Prefect) para coleta incremental diária
* Camada de testes unitários + cobertura CI em GitHub Actions
* Containerização com Docker Compose (DB + App)
* Alertas de anomalia (SMA/EMA/RSI) push para Slack/Teams
* Integração com BigQuery/Data Studio para democratização dos dados

---

## 🧰 Stack

| Camada       | Tecnologia                          |
| ------------ | ----------------------------------- |
| Linguagem    | Python 3.10 + type hints            |
| Ingestão     | `requests`, `pandas`                |
| Persistência | SQLAlchemy ORM (SQLite por default) |
| Visualização | Streamlit + Matplotlib              |
| Configuração | python-dotenv                       |
| Deploy Demo  | Streamlit Cloud                     |

---

## 📌 Observações

* Alguns ativos da CoinCap não expõem histórico; esses registros são ignorados sem interromper o fluxo, assegurando **idempotência** e **alta disponibilidade** da pipeline.
* A solução é **state-of-the-art friendly**: facilmente plugável em GCP/AWS (Cloud SQL, S3, Lambda) ou pipelines Spark/Databricks.

---

## 👨‍💻 Autor

**Leandro Vidigal** — Senior Data Engineer
[LinkedIn](https://www.linkedin.com/in/leandrovidigal) 
