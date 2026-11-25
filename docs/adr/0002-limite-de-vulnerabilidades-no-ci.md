# 0002: Limite de vulnerabilidades no CI

- Status: aceito
- Data: 24/11/2026
- Revisão: 24/02/2027

## Contexto

O job `dependencias` do CI (`actions/dependency-review-action`) compara as
dependências de cada PR com a `main` e hoje bloqueia apenas vulnerabilidades
**críticas** (`fail-on-severity: critical`), como no modelo da disciplina (PGC 5.3).

Situação em 24/11/2026:

- **Dependabot alerts:** ativo, **nenhum alerta** aberto em nenhuma severidade.
- **Secret scanning:** ativo, sem segredos detectados.
- **Dependências de produção** (vão para a imagem): `pandas` e `psycopg[binary]`,
  mais as imagens `python:3.12-slim-trixie` (Dockerfile) e `postgres:16.15-bookworm`
  (docker-compose).
- **Dependências de desenvolvimento** (só CI e máquina local): `pytest`,
  `pytest-cov` e `ruff`.

O FundScope processa dados públicos da CVM e não recebe entrada de usuários
externos, mas a imagem lê arquivos baixados da internet e grava no PostgreSQL.
Uma vulnerabilidade `high` no `pandas` (leitura de CSV) ou no `psycopg` (conexão
com o banco) afetaria diretamente a produção.

## Decisão

1. **Subir o limite do CI de `critical` para `high`.** Como não há alertas
   abertos, a mudança não bloqueia nenhum PR hoje e passa a impedir que uma
   dependência com vulnerabilidade `high` entre na `main`.
2. **Aceitar o risco de `moderate` e `low`:** não bloqueiam o merge. Ficam
   visíveis em **Security → Dependabot alerts** e são tratadas pelos PRs
   automáticos do Dependabot.
3. **Atualização de segurança em dependência de produção usa `fix(deps): ...`**
   no título do PR, e não `chore(deps)`, para gerar uma versão PATCH e chegar à
   produção sem esperar o próximo `feat` ou `fix` (ver ADR 0001).

A mudança no `ci.yml` (`fail-on-severity: high`) é feita em um PR `ci:` próprio,
que referencia este ADR.

## Alternativas consideradas

- **Manter `critical`:** é o padrão da disciplina, mas aceitaria em produção uma
  vulnerabilidade `high` no `pandas` ou no `psycopg` sem nenhuma decisão
  registrada. Com zero alertas, não há custo que justifique aceitar esse risco.
- **Bloquear também `moderate`:** aumenta a proteção, mas alertas `moderate` são
  frequentes e muitas vezes sem correção disponível; travaria PRs sem relação com
  a dependência afetada.
- **Bloquear só dependências de produção:** a action permite filtrar por escopo,
  mas o projeto ainda é pequeno e o ganho não compensa a configuração extra.

## Consequências

- Um PR que introduza dependência com vulnerabilidade `high` ou `critical` fica
  bloqueado pelo `ci-ok` até a versão ser trocada.
- Alertas `moderate` e `low` podem existir na `main`: risco aceito e documentado,
  acompanhado pelos alertas do Dependabot.
- Se uma vulnerabilidade `high` sem correção disponível bloquear o trabalho, a
  exceção deve ser registrada em uma Issue de CCM (PGC 8.2), com prazo.
- **Revisão em 24/02/2027:** conferir quantos alertas surgiram e quantos PRs foram
  bloqueados, e decidir se o limite continua em `high`.
