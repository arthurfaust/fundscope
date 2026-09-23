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

Ambiente Python configurado e pacote inicial executável.
Ruff, Pytest e pytest-cov instalados.

O pipeline de dados, os testes e os workflows de CI/CD
ainda serão implementados.

## Preparar o ambiente

    git clone https://github.com/arthurfaust/fundscope.git
    cd fundscope
    uv sync --locked

## Executar o exemplo inicial

    uv run fundscope

## Verificar o código

    uv run ruff check .

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

Nesta etapa, a aplicação imprime uma mensagem inicial e encerra.

## Parar o ambiente

    docker compose down

O volume do PostgreSQL é preservado. A opção `down -v` remove
os volumes e apaga os dados locais do banco.