# 🌍 Earth Sismos

> Pipeline de dados sísmicos globais com foco especial no Brasil.  
> Stack: DLT · DuckDB · dbt · Metabase · RAG (notícias Brasil)  
> Fonte primária: [USGS Earthquake Hazards API](https://earthquake.usgs.gov/fdsnws/event/1/)

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![dbt](https://img.shields.io/badge/dbt-Core-orange)
![DuckDB](https://img.shields.io/badge/DuckDB-OLAP-green)
![Metabase](https://img.shields.io/badge/Metabase-self--hosted-509EE3)

---

## 📋 Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Stack tecnológica](#stack-tecnológica)
- [Setup](#setup)
- [Como usar](#como-usar)
- [Dashboards](#dashboards)
- [Progresso do projeto](#progresso-do-projeto)

---

## Sobre o projeto

O **Earth Sismos** é um pipeline de dados de ponta a ponta que ingere, transforma e visualiza dados sísmicos globais da API do USGS. O projeto tem atenção especial ao Brasil, incluindo histórico completo de eventos por estado e um módulo RAG que gera contexto textual automático a partir de notícias sobre os tremores.

**O que o projeto entrega:**
- Histórico de 10 anos de terremotos globais
- Histórico completo de terremotos no Brasil por estado
- Dashboards interativos com mapa-múndi em tempo real (últimas 24h)
- Rankings históricos por país e por evento
- Textos de contexto gerados por IA sobre eventos significativos no Brasil

---

## Arquitetura

```
USGS API
    │
    ▼
┌─────────────────────────────────┐
│  INGESTÃO — Python + DLT        │
│  • Carga histórica (10 anos)    │
│  • Incremental a cada 6h        │
│  • Brasil: histórico completo   │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  BRONZE — DuckDB                │
│  • Dados brutos da API          │
│  • Schema raw, sem transformação│
│  • Particionado por data        │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  SILVER — dbt + dbt tests       │
│  • Limpeza e padronização       │
│  • Tipagem e validação          │
│  • Deduplicação e enriquecimento│
│    geográfico (país, região)    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  GOLD — dbt                     │
│  • Agregações por região/país   │
│  • Rankings históricos          │
│  • Série temporal por estado BR │
│  • Contexto RAG (notícias BR)   │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  METABASE                       │
│  • Dashboard: dados globais     │
│  • Mapa-múndi: últimas 24h      │
│  • Histórico por país / ranking │
│  • Painel Brasil por estado     │
└─────────────────────────────────┘
```

---

## Stack tecnológica

| Camada | Ferramenta | Justificativa |
|---|---|---|
| Ingestão | Python + DLT | Pipelines declarativos, suporte nativo a incremental e histórico |
| Armazenamento | DuckDB | OLAP local sem servidor, perfeito para este volume |
| Transformação | dbt Core | Modelos SQL versionados, testes nativos de qualidade |
| Qualidade | dbt tests | Cobertura de nulidade, unicidade e integridade referencial |
| Visualização | Metabase (self-hosted) | Suporte a mapas, open source, conecta direto no DuckDB |
| Contexto textual | RAG com notícias (Brasil) | NewsAPI + embeddings + LLM local via Ollama |
| Orquestração | Cron / Airflow | Trigger da carga incremental a cada 6h |

---

## Setup

### Pré-requisitos

- Python 3.11+
- Docker (para o Metabase)
- Git

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/earth-sismos.git
cd earth-sismos

# 2. Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com seus valores
```

### Variáveis de ambiente (`.env`)

```env
USGS_BASE_URL=https://earthquake.usgs.gov/fdsnws/event/1/query
DUCKDB_PATH=data/sismos.duckdb
NEWSAPI_KEY=sua_chave_aqui   # necessário apenas para o módulo RAG
```

---

## Como usar

### Carga histórica (primeira execução)

```bash
# Histórico global — 10 anos, fatiado por trimestre
python ingestao/pipeline_global.py --mode=historical

# Histórico completo do Brasil
python ingestao/pipeline_brasil.py --mode=historical
```

### Carga incremental

```bash
# Execução manual
python ingestao/pipeline_global.py --mode=incremental

# Via cron (a cada 6 horas)
0 */6 * * * cd /path/earth-sismos && python ingestao/pipeline_global.py --mode=incremental
```

### Transformações dbt

```bash
cd dbt_sismos

# Rodar todos os modelos
dbt build

# Rodar apenas Silver ou Gold
dbt run --select silver
dbt run --select gold

# Rodar os testes
dbt test

# Ver a documentação
dbt docs generate && dbt docs serve
```

### Metabase

```bash
# Subir o Metabase via Docker
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

Acesse `http://localhost:3000` e configure a conexão com o arquivo `data/sismos.duckdb`.

---

## Dashboards

| Dashboard | Descrição |
|---|---|
| 📊 Dados Globais | Visão analítica: totais por período, distribuição de magnitudes, série temporal |
| 🗺️ Mapa-múndi 24h | Mapa de pontos em tempo real com todos os terremotos das últimas 24 horas |
| 🏆 Ranking Histórico | Top eventos mundiais, histórico por país, mapa de calor de atividade sísmica |
| 🇧🇷 Painel Brasil | Eventos por estado, série histórica, maior eventos BR + contexto gerado por IA |

> 🔗 Links para os dashboards públicos serão adicionados após o deploy.

---

## Progresso do projeto

### ⚙️ Ambiente

- [ ] Repositório criado e configurado no GitHub
- [ ] Ambiente virtual Python configurado
- [ ] Dependências instaladas (`requirements.txt`)
- [ ] Arquivo `.env` configurado
- [ ] `.gitignore` com `data/`, `.env`, `.venv/`

---

### 📥 Ingestão (Camada Bronze)

- [ ] `ingestao/config.py` com parâmetros centralizados
- [ ] `ingestao/utils.py` com função de fatiamento de janelas temporais
- [ ] `ingestao/pipeline_global.py`:
  - [ ] Carga histórica (loop por trimestres)
  - [ ] Carga incremental com cursor de estado DLT
  - [ ] Tratamento de erros e retry com backoff exponencial
- [ ] Carga histórica global executada e validada no DuckDB
- [ ] `ingestao/pipeline_brasil.py`:
  - [ ] Carga histórica completa com janelas mensais
  - [ ] Enriquecimento de estado via reverse geocoding (`geopy`)
- [ ] Carga histórica Brasil executada e validada no DuckDB
- [ ] Cron ou Airflow configurado para incremental a cada 6h

---

### 🥈 Transformação Silver (dbt)

- [ ] Projeto dbt inicializado (`dbt init dbt_sismos`)
- [ ] `profiles.yml` configurado para DuckDB local
- [ ] Seed: tabela países → continentes → sub-regiões
- [ ] Seed: estados brasileiros → regiões do Brasil
- [ ] Modelo `stg_terremotos_raw.sql` (staging Bronze)
- [ ] Modelo `dim_terremotos.sql`:
  - [ ] Cast de tipos e filtros
  - [ ] Deduplicação por `id`
  - [ ] Classificação de magnitude (`micro` → `grandioso`)
  - [ ] Extração de país/região do campo `place`
  - [ ] Flag `is_brasil`
- [ ] Modelo `dim_localizacao.sql` (enriquecimento geográfico)
- [ ] `schema.yml` com testes de qualidade (unique, not_null, accepted_range)
- [ ] `dbt test` passando com 0 falhas
- [ ] `dbt docs` gerado e revisado

---

### 🥇 Agregações Gold (dbt)

- [ ] Modelo `agg_terremotos_24h.sql` (alimenta mapa em tempo real)
- [ ] Modelo `agg_terremotos_pais.sql` (histórico por país e ano)
- [ ] Modelo `ranking_historico_pais.sql` (top N eventos por país)
- [ ] Modelo `serie_temporal_brasil.sql` (por estado, mês e ano)
- [ ] Modelo `eventos_brasil_contexto.sql` (eventos BR + campo RAG)
- [ ] `schema.yml` para modelos Gold com testes básicos
- [ ] `dbt build` completo (Silver + Gold) sem erros
- [ ] Validação por amostragem:
  - [ ] `agg_terremotos_24h` — eventos recentes presentes
  - [ ] `agg_terremotos_pais` — 180+ países distintos
  - [ ] `serie_temporal_brasil` — 27 UFs presentes

---

### 📊 Metabase (Dashboards)

- [ ] Metabase rodando via Docker
- [ ] Conexão com `sismos.duckdb` configurada
- [ ] Dashboard 1 — Dados Globais criado e validado
- [ ] Dashboard 2 — Mapa-múndi 24h criado e testado
- [ ] Dashboard 3 — Histórico e Ranking por País criado
- [ ] Dashboard 4 — Painel Brasil criado
- [ ] Dashboards configurados como públicos (sem login)
- [ ] Testado em dispositivo móvel

---

### 🤖 RAG — Contexto Textual (opcional)

- [ ] Conta criada na NewsAPI e chave salva no `.env`
- [ ] `rag/coletor_noticias.py` — busca e salva artigos por evento
- [ ] `rag/embeddings.py` — chunking + geração de vetores (ChromaDB)
- [ ] `rag/retriever.py` — busca por similaridade dado um evento
- [ ] `rag/gerador_texto.py` — prompt + LLM (OpenAI ou Ollama local)
- [ ] Campo `contexto_textual` integrado em `eventos_brasil_contexto`
- [ ] Card de texto no Dashboard 4 (Brasil) exibindo o contexto gerado
- [ ] Testado com 5 eventos históricos significativos do Brasil

---

### 🚀 Publicação

- [ ] README completo com screenshots dos dashboards
- [ ] `ARCHITECTURE.md` com decisões técnicas documentadas
- [ ] Links para dashboards públicos adicionados ao README
- [ ] Post no LinkedIn publicado
- [ ] Projeto adicionado ao portfólio

---

## Estrutura do repositório

```
earth-sismos/
├── ingestao/
│   ├── pipeline_global.py
│   ├── pipeline_brasil.py
│   ├── config.py
│   └── utils.py
├── dbt_sismos/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   └── tests/
├── rag/
│   ├── coletor_noticias.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── gerador_texto.py
├── metabase/
│   └── README.md
├── orquestracao/
│   └── crontab.txt
├── data/                  # não versionado
│   └── sismos.duckdb
├── .env.example
├── requirements.txt
└── README.md
```

---

## Referências

| Recurso | Link |
|---|---|
| USGS API | https://earthquake.usgs.gov/fdsnws/event/1/ |
| DLT Docs | https://dlthub.com/docs/intro |
| dbt-duckdb | https://github.com/duckdb/dbt-duckdb |
| dbt-utils | https://hub.getdbt.com/dbt-labs/dbt_utils/latest/ |
| Metabase Docker | https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker |
| ChromaDB | https://docs.trychroma.com |
| Ollama | https://ollama.com |
| NewsAPI | https://newsapi.org |
| sentence-transformers | https://www.sbert.net |

---

*Projeto: Earth Sismos — Igor Tiburcio · Iniciado em abril de 2026*
