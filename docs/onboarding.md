# Guia de onboarding: FundScope

Este guia basta para preparar o ambiente, rodar os testes e abrir o seu primeiro
Pull Request sem precisar perguntar nada a ninguém (PGC 12). Se algo aqui estiver
confuso ou errado, corrija o próprio guia num PR `docs: ...`.

## 1. Pré-requisitos

| Ferramenta | Versão | Como conferir |
|---|---|---|
| Git | qualquer recente | `git --version` |
| uv | 0.12.17 ou mais recente | `uv --version` |
| Docker com Compose | opcional, só para o PostgreSQL e a imagem | `docker compose version` |

- Instalar o uv: <https://docs.astral.sh/uv/getting-started/installation/>.
  O uv instala o Python 3.12 sozinho; não é preciso instalar o Python antes.
- **Windows:** use o WSL ou o **Git Bash**. O PowerShell padrão não aceita `&&`.
- **Rede do laboratório:** a porta 22 costuma estar bloqueada; clone por `https://`.

## 2. Preparar o ambiente

```bash
git clone https://github.com/arthurfaust/fundscope.git
cd fundscope
uv sync --locked --dev
```

O `--locked` garante as mesmas versões do `uv.lock` usadas pelo CI. O `--dev`
instala também pytest, pytest-cov e ruff.

## 3. Rodar a verificação que o CI faz

Rode estes comandos antes de abrir um PR. Se passarem aqui, passam no CI.

```bash
uv run ruff format --check .
uv run ruff check .
uv run python -m pytest tests/unit --cov=fundscope --cov-report=term-missing
```

- Use `python -m pytest`, e não só `pytest`.
- Se `ruff format --check` reclamar, rode `uv run ruff format .` e confira a diferença.
- Se aparecer `Failed to spawn: pytest` ou `No such file or directory`, o `.venv`
  foi criado em outra pasta. Recrie com `rm -rf .venv && uv sync --locked --dev`.

## 4. PostgreSQL local (opcional)

Só é necessário para rodar a carga no banco; os testes unitários não usam banco.

```bash
cp .env.example .env
```

Preencha `POSTGRES_PASSWORD` no `.env`. O `.env` nunca vai para o Git. Depois:

```bash
docker compose up -d --wait postgres
docker compose ps
```

Os schemas `silver`, `gold` e `metadata` são criados automaticamente pelo
`sql/schema.sql`. Para parar: `docker compose down` (o `down -v` apaga os dados).

## 5. Seu primeiro Pull Request

A `main` é protegida: ninguém faz push direto nela. Toda mudança entra por PR.

1. **Issue:** escolha ou crie uma Issue (**Issues → New issue**, formulário
   *Funcionalidade* ou *Defeito*) e atribua a você.
2. **Branch** a partir da `main` atualizada:
   ```bash
   git switch main && git pull
   git switch -c feature/<numero-da-issue>-<descricao-curta>
   ```
   Prefixos: `feature/`, `fix/`, `docs/`, `ci/`, `chore/`, `revert/`.
3. **Commits** pequenos, em Conventional Commits:
   `fix(transform): trata data vazia no informe`.
4. **Envie e abra o PR:**
   ```bash
   git push -u origin <nome-da-branch>
   ```
   No GitHub, clique em **Compare & pull request**.
5. **Título do PR** em Conventional Commits. Ele vira a mensagem do commit na
   `main` (squash merge) e define a próxima versão:

   | Título | Efeito |
   |---|---|
   | `feat: ...` | nova versão MINOR (1.1.0 → 1.2.0) |
   | `fix: ...` ou `perf: ...` | nova versão PATCH (1.1.0 → 1.1.1) |
   | `docs`, `chore`, `ci`, `test`, `refactor`, `style`, `revert` | sem versão nova |

6. **Descrição:** preencha o template (Contexto, Decisão tomada, Como testar e
   checklist) e escreva `Closes #<numero-da-issue>` no final.
7. **Revisão:** o CODEOWNERS pede a revisão automaticamente. É preciso 1 aprovação
   de outra pessoa; ninguém aprova o próprio PR.
8. **Merge:** com os checks verdes e a aprovação, use **Squash and merge**.

## 6. Lendo o resultado do pipeline

Na aba **Checks** do PR:

| Check | O que verifica | Se ficar vermelho |
|---|---|---|
| `titulo-pr` | título do PR em Conventional Commits | edite o título; o check roda de novo sozinho |
| Qualidade e testes | formatação e lint (Ruff), testes, cobertura, build da imagem e integração com PostgreSQL | **Details** → abra o passo com ❌ e leia o erro |
| Análise de dependências (SCA) | vulnerabilidade alta ou crítica nas dependências alteradas pelo PR (ADR 0002) | troque a versão da dependência indicada |
| `ci-ok` | resumo: todos os anteriores passaram ou foram pulados | veja qual job acima dele falhou |

Só `ci-ok` e `titulo-pr` são obrigatórios. A Análise de dependências fica *skipped*
fora de PRs; isso é normal.

**Branch desatualizada:** se aparecer *This branch is out-of-date with the base
branch*, clique em **Update branch**. O CI roda de novo e a aprovação precisa ser
renovada.

## 7. Depois do merge

O workflow **CD** (aba **Actions**) roda sozinho:

1. **Versão e imagem:** calcula a versão e constrói a imagem
   `ghcr.io/arthurfaust/fundscope:sha-<commit>`.
2. **Staging:** executa a imagem e marca a tag `staging`.
3. **Produção:** só para `feat` e `fix`. Fica em *Waiting* até o desenvolvedor
   líder (`arthurfaust`) aprovar; então cria a tag `vX.Y.Z` e a Release.

Mudanças só em `docs/` ou arquivos `.md` não disparam o CD.

## 8. Onde encontrar o resto

| Assunto | Onde |
|---|---|
| Plano de Gerência de Configuração | `docs/Plano GCPS - FundScope.pdf` |
| Decisões de arquitetura | `docs/adr/` |
| Evidências de configuração e das aulas | `docs/evidencias/` |
| Versões publicadas | **Releases** do repositório |
| Mudança de alto risco (banco, LGPD, hotfix) | **Issues → New issue → Mudança de alto risco (CCM)** |
| Dúvidas | abra uma Issue ou comente no PR |
