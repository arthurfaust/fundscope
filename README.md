# FundScope

Projeto acadêmico da disciplina de Gerenciamento, Configuração
e Processos de Software, com foco em práticas DevOps aplicadas
a um pipeline de dados públicos de fundos de investimento da CVM.

## Objetivo

Coletar, validar e transformar dados da CVM nas camadas Bronze,
Silver e Gold, disponibilizando informações em um dashboard.

## Tecnologias previstas

Python, Pandas, PostgreSQL, Apache Airflow, Streamlit,
Docker Compose, uv e GitHub Actions.

## Estado atual

- Fluxo inicial Bronze -> Silver implementado em
  `src/fundscope/pipeline.py`: leitura do CSV da CVM, validação,
  transformação e carga no PostgreSQL.
- Testes unitários da camada de validação. O CI exige 80% de
  cobertura nessa camada e 18% no pacote inteiro (valor atual,
  com plano registrado em Issue para chegar a 60%).
- PostgreSQL local via Docker Compose, com os schemas silver,
  gold e metadata.
- CI (qualidade, testes, build e integração com PostgreSQL) e
  CD (publicação da imagem Docker no GHCR) no GitHub Actions.

Ainda serão implementados a orquestração com Airflow, a camada
Gold e o dashboard em Streamlit.

## Estrutura do repositório

    .
    ├── .github/             # Templates de PR e Issue, CODEOWNERS
    │   └── workflows/       # CI (ci.yml), título do PR (pr-titulo.yml) e CD (cd.yml)
    ├── docs/                # Plano de GCS e evidências
    │   └── evidencias/      # Prints e logs das configurações
    ├── sql/                 # Script de criação dos schemas
    ├── src/fundscope/       # Código-fonte do pacote
    │   ├── extract/         # Download dos arquivos da CVM (Bronze)
    │   ├── validation/      # Validação de colunas e dados
    │   ├── transform/       # Transformação Bronze -> Silver
    │   ├── load/            # Carga no PostgreSQL
    │   ├── pipeline.py      # Orquestração do fluxo
    │   └── healthcheck.py   # Verificação do banco no container
    ├── tests/unit/          # Testes unitários
    ├── Dockerfile           # Imagem da aplicação
    ├── docker-compose.yml   # PostgreSQL e serviço da aplicação
    ├── pyproject.toml       # Dependências e configuração do pacote
    └── uv.lock              # Versões travadas das dependências

## Gerência de configuração

O plano de Gerência de Configuração de Software está em
[docs/Plano GCPS - FundScope.pdf](docs/Plano%20GCPS%20-%20FundScope.pdf).

Resumo das práticas adotadas:

- **Branch protegida:** a `main` não aceita push direto. Toda
  mudança entra por pull request, com aprovação de um revisor e
  os checks obrigatórios `ci-ok` e `titulo-pr` aprovados.
- **Revisão em par:** um colaborador com acesso de escrita revisa
  e aprova os pull requests.
- **Branches de trabalho:** `feature/*`, `fix/*`, `docs/*`,
  `ci/*` e `chore/*`, integradas à `main` por pull request.
- **Merge:** somente *squash merge*. Cada pull request vira um
  único commit na `main`, com o título do PR como mensagem, e a
  branch de origem é apagada após o merge.
- **Commits e títulos de PR:** padrão Conventional Commits
  (`feat`, `fix`, `docs`, `ci`, `test`, `chore`, `refactor`).
- **Modelos de colaboração:** template de pull request com o
  checklist de revisão, templates de Issue (funcionalidade e
  defeito) e `CODEOWNERS`, em `.github/`.
- **Environments:** `staging` e `production`, usados pelo CD e
  restritos à branch `main`. O `production` exige aprovação de
  `arthurfaust` antes da promoção da imagem.

### Evidências

Os registros das configurações estão em
[docs/evidencias/](docs/evidencias/):

| Evidência | Arquivo |
|---|---|
| Regras de proteção da `main` | `protecao_main1.png`, `protecao_main2.png`, `protecao_main3.png` |
| Push direto na `main` recusado | `push_direto_recusado.png`, `push-direto-recusado.txt` |
| Colaborador com acesso de escrita | `contribuidores.png` |

## Preparar o ambiente

    git clone https://github.com/arthurfaust/fundscope.git
    cd fundscope
    uv sync --locked

## Executar o exemplo inicial

    uv run fundscope

## Verificar o código

    uv run ruff format --check .
    uv run ruff check .

## Executar os testes

    uv run python -m pytest tests/unit --cov=fundscope --cov-report=term-missing

## Ambiente local com Docker

Pré-requisito: Docker com Docker Compose.

1. Copie `.env.example` para `.env`.
2. Preencha `POSTGRES_PASSWORD` no `.env`.
3. Inicie o PostgreSQL:

       docker compose up -d --wait postgres

4. Confira o estado do serviço:

       docker compose ps

Em um volume novo, os schemas silver, gold e metadata são
criados automaticamente pelo script sql/schema.sql.

Para aplicar o script em um banco já inicializado:

    docker compose exec -T postgres psql -U fundscope -d fundscope -v ON_ERROR_STOP=1 < sql/schema.sql

## Executar a aplicação em container

    docker build -t fundscope/app:dev .
    docker run --rm fundscope/app:dev

Para verificar a conexão do container com o PostgreSQL:

    docker compose run --rm app

## Integração e entrega contínuas

- **CI** (`.github/workflows/ci.yml`): roda em pull requests e
  pushes na `main`, com três jobs:
  1. **Qualidade e testes:** formatação e lint com Ruff, testes
     com quality gate de cobertura, validação do Docker Compose,
     build da imagem e integração com o PostgreSQL.
  2. **Análise de dependências (SCA):** compara as dependências
     do PR com a `main` e bloqueia vulnerabilidades críticas.
  3. **ci-ok:** agrega os anteriores; é o único check de CI
     marcado como obrigatório na proteção da `main`.
- **Título do PR** (`.github/workflows/pr-titulo.yml`): o check
  `titulo-pr` valida se o título segue Conventional Commits, pois
  ele vira a mensagem do commit na `main` após o squash.
- **CD** (`.github/workflows/cd.yml`): roda a cada merge na
  `main` e publica a imagem em `ghcr.io/arthurfaust/fundscope`
  em duas etapas:
  1. **staging:** constrói a imagem, verifica a execução do
     container e publica as tags `sha-<commit>` e `staging`.
  2. **production:** aguarda a aprovação do revisor obrigatório
     e promove a mesma imagem, sem reconstruir, para as tags
     `production` e `latest`.

## Parar o ambiente

    docker compose down

O volume do PostgreSQL é preservado. A opção `down -v` remove
os volumes e apaga os dados locais do banco.
