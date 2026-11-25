# Guia de onboarding: FundScope

Este guia basta para preparar o ambiente, rodar os testes e abrir o seu primeiro
Pull Request sem precisar perguntar nada a ninguém (PGC 12). Se algo aqui estiver
confuso ou errado, corrija o próprio guia num PR `docs: ...`.

## 1. Pré-requisitos

| Ferramenta | Versão | Como conferir |
|---|---|---|
| Git | qualquer recente | `git --version` |
| uv | 0.12.17, a mesma usada pelo CI | `uv --version` |
| Docker com Compose | opcional, só para o PostgreSQL e a imagem | `docker compose version` |

Instale o uv pelo instalador oficial, usando o comando do seu terminal:

**Windows (PowerShell):**

```powershell
Invoke-RestMethod https://astral.sh/uv/0.12.17/install.ps1 | Invoke-Expression
```

**Linux, macOS ou WSL (Bash):**

```bash
curl -LsSf https://astral.sh/uv/0.12.17/install.sh | sh
```

Feche e abra o terminal depois da instalação e confira `uv --version`.
Se `uv` não for reconhecido, verifique se a pasta informada pelo instalador
está no `PATH` desse terminal. Outras opções de instalação estão em
<https://docs.astral.sh/uv/getting-started/installation/>.

- O uv baixa o Python 3.12 indicado em `.python-version` durante o `uv sync`;
  não é preciso instalar o Python nem ativar o ambiente virtual manualmente.
- Use a versão do uv indicada acima para reproduzir o CI. Uma versão mais nova
  pode mostrar um aviso de incompatibilidade com o intervalo de `uv_build`
  definido em `pyproject.toml`.
- **Windows:** os passos 2 e 3 funcionam no PowerShell, executando um comando
  por linha. O Windows PowerShell 5.1 não aceita `&&`; o PowerShell 7 aceita.
  WSL e Git Bash são alternativas. Mantenha instalação e execução no mesmo
  ambiente: o uv instalado no Windows não equivale a uma instalação no WSL.
- **Rede do laboratório:** a porta 22 costuma estar bloqueada; clone por `https://`.

## 2. Preparar o ambiente

Abra o terminal na pasta onde deseja criar a cópia do projeto. O clone cria
uma subpasta chamada `fundscope`; não execute o comando dentro de outra cópia.
Os comandos abaixo funcionam em PowerShell e Bash, um por linha:

```text
git clone https://github.com/arthurfaust/fundscope.git
cd fundscope
uv sync --locked --dev
```

Execute os próximos comandos dentro de `fundscope`, onde estão `pyproject.toml`
e `uv.lock`. A primeira sincronização precisa de internet para baixar o Python
e as dependências e cria o ambiente virtual local `.venv`.

O `--locked` exige que `uv.lock` esteja atualizado e usa as versões fixadas
nele. O `--dev` instala também pytest, pytest-cov e ruff. Se o comando falhar,
resolva o erro antes de continuar; não remova `--locked` nem atualize o lockfile
apenas para contornar uma falha de instalação.

## 3. Rodar as verificações locais de qualidade e testes

Rode os comandos abaixo antes de abrir um PR. Eles reproduzem a formatação,
o lint e os limites de cobertura do CI, mas não garantem que todo o CI passe:
o workflow também verifica Docker, integração com PostgreSQL, título do PR
e dependências. Para os comandos desta seção, Docker, banco e `.env` não são
necessários.

```text
uv run --locked ruff format --check .
uv run --locked ruff check .
uv run --locked python -m pytest tests/unit --cov=fundscope --cov-report=term-missing --cov-fail-under=18
uv run --locked python -m coverage report --include="*/fundscope/validation/*" --fail-under=80
```

Execute um comando por vez e confira o resultado antes de seguir. A última
verificação usa o arquivo `.coverage` gerado pelo pytest; rode-a depois dos
testes. Os limites atuais são 18% para o pacote completo e 80% para a camada
de validação, conforme `.github/workflows/ci.yml`.

- Use `python -m pytest`, e não só `pytest`.
- Se `ruff format --check` reclamar, rode `uv run --locked ruff format .` e
  confira a diferença antes de incluir arquivos no commit.
- Se aparecer `Failed to spawn: pytest` ou `No such file or directory`, confira
  primeiro a pasta atual e rode `uv sync --locked --dev`. A mensagem sozinha
  não comprova que o ambiente foi criado em outra pasta.
- Não copie nem compartilhe `.venv` entre pastas, Windows e WSL. Se o ambiente
  foi movido ou copiado e o erro persistir, recrie somente a `.venv` da cópia
  atual. Confirme que está na raiz correta antes de executar:

  **PowerShell:**
  ```powershell
  Remove-Item -LiteralPath .venv -Recurse -Force
  uv sync --locked --dev
  ```

  **Bash:**
  ```bash
  rm -rf .venv
  uv sync --locked --dev
  ```

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
   git switch main
   git pull --ff-only
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
