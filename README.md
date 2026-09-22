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