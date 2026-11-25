# Evidências: Aula 4, Governança

Seções do PGC aplicadas: 8.2 (CCM), 10 (auditoria e rastreabilidade), 12 (onboarding) e 13 (dependências).

Issue de acompanhamento: [#26: chore: configurar governanca conforme Aula 4](https://github.com/arthurfaust/fundscope/issues/26)

## 1. Dependências como itens de configuração (PGC 13)

| Item | Situação |
|---|---|
| Dependabot alerts | ativo; nenhum alerta em 24/11/2026 |
| Secret scanning | ativo |
| `.github/dependabot.yml` | [PR #27](https://github.com/arthurfaust/fundscope/pull/27): ecossistemas `uv`, `docker`, `docker-compose` e `github-actions`, todos com prefixo `chore(deps)` |

Exclusões registradas no arquivo: Python minor/major (decisão do projeto) e
PostgreSQL major (exige migração de dados, mudança de alto risco).

### PRs do Dependabot revisados

| PR | Atualização | Revisão e justificativa | Resultado |
|---|---|---|---|
| [#29](https://github.com/arthurfaust/fundscope/pull/29) | pandas 3.0.6 → 3.1.1 (produção) | [comentário](https://github.com/arthurfaust/fundscope/pull/29#issuecomment-7149370342): notas da 3.1 sem mudanças nas funções usadas em `transform/informes.py`; CI verde | mesclado |
| [#28](https://github.com/arthurfaust/fundscope/pull/28) | astral-sh/setup-uv 9.0.0 → 10.4.0 (major, CI) | [comentário](https://github.com/arthurfaust/fundscope/pull/28#issuecomment-7149410442): única mudança incompatível (cache em `pull_request_target`, `workflow_run`, `release`) não afeta o CI; [aprovado por mariagranza](https://github.com/arthurfaust/fundscope/pull/28#pullrequestreview-6050082111) | mesclado |

Ocorrência: no #28, a regra *Require branches to be up to date* exigiu atualizar a
branch depois do merge do #29. O Dependabot não respondeu ao `@dependabot rebase` em
25 minutos e a branch foi atualizada pelo botão *Update branch*
([registro](https://github.com/arthurfaust/fundscope/pull/28#issuecomment-7149950428)).
Assim, a combinação pandas 3.1.1 + setup-uv 10.4.0 foi testada antes do merge.

## 2. Aceitação de risco registrada

Decisão no [ADR 0002](../adr/0002-limite-de-vulnerabilidades-no-ci.md): o CI passa a
bloquear vulnerabilidades `high` e `critical`; `moderate` e `low` são risco aceito.
Revisão em **24/02/2027**. Implementação: [PR #31](https://github.com/arthurfaust/fundscope/pull/31).

## 3. Comitê de Controle de Mudanças (PGC 8.2)

| Item | Link |
|---|---|
| Formulário | `.github/ISSUE_TEMPLATE/mudanca-alto-risco.yml` ([PR #27](https://github.com/arthurfaust/fundscope/pull/27)) |
| Issue de mudança de alto risco | [#35: Adicionar restrição de CNPJ válido na tabela silver.informe_diario](https://github.com/arthurfaust/fundscope/issues/35), aberta pelo desenvolvedor líder |
| Critério de risco | altera a estrutura do banco com dados já carregados |
| Plano de rollback | backup com `pg_dump`, `DROP CONSTRAINT` e retorno da aplicação para a **v1.0.1** pelo workflow Rollback |
| Perguntas do comitê | [mariagranza](https://github.com/arthurfaust/fundscope/issues/35#issuecomment-7151035595): registros inválidos, versão em produção e backup |
| Respostas do proponente | [arthurfaust](https://github.com/arthurfaust/fundscope/issues/35#issuecomment-7151167556) |
| Decisão do par (comitê) | [**Aprovada com ressalvas**, por mariagranza](https://github.com/arthurfaust/fundscope/issues/35#issuecomment-7151220760) |

Ressalvas registradas pelo comitê: anexar na Issue a versão validada em staging, as
contagens antes e depois da limpeza e o teste de restauração; exportar os registros
afetados antes de excluí-los; limpeza e restrição na mesma transação, sem cargas
concorrentes; tratar `NULL` se a coluna não for `NOT NULL`; documentar o local e a
retenção do backup. A mudança não foi implementada: o exercício é a decisão registrada.

Ocorrência: a proposta foi aberta primeiro pela conta do par ([#33](https://github.com/arthurfaust/fundscope/issues/33)
e [#34](https://github.com/arthurfaust/fundscope/issues/34)). Pelo PGC 8.2, quem propõe
é o desenvolvedor líder e o par atua na análise e na decisão; as duas foram fechadas
como duplicadas e a proposta foi reaberta na #35.

## 4. Registros de decisão de arquitetura

[PR #30: docs: registra decisões de arquitetura](https://github.com/arthurfaust/fundscope/pull/30)
(não gerou versão nem disparou o CD):

- [0001: Produção é a imagem no GHCR mais a Release do GitHub](../adr/0001-producao-imagem-ghcr-e-release.md)
- [0002: Limite de vulnerabilidades no CI](../adr/0002-limite-de-vulnerabilidades-no-ci.md) (risco aceito, com prazo de revisão)

## 5. Onboarding testado (PGC 12)

| Item | Link |
|---|---|
| Guia | [docs/onboarding.md](../onboarding.md) ([PR #32](https://github.com/arthurfaust/fundscope/pull/32)) |
| PR do par seguindo o guia sem ajuda | [#36: docs: esclarece instalacao e verificacoes do onboarding no Windows](https://github.com/arthurfaust/fundscope/pull/36), aberto por mariagranza |

O teste foi feito no Windows com PowerShell 7, uv 0.12.17 e Python 3.12, até o passo 3
(Docker opcional não executado). O par encontrou e corrigiu no próprio guia:

- instalação do uv sem comando por sistema e sem orientação sobre o `PATH`;
- orientação para Windows imprecisa (PowerShell 5.1 x 7, WSL x Windows);
- comandos sem os limites de cobertura do CI (18% no pacote, 80% na validação);
- a afirmação de que passar nas verificações locais garantia o CI inteiro;
- uma causa única atribuída ao erro `Failed to spawn: pytest`.

Na revisão, ficou registrado que os limites de cobertura agora aparecem no guia e no
`ci.yml`: quando a #14 elevar o gate para 60%, os dois precisam mudar juntos.

## 6. Rastreabilidade de ponta a ponta (PGC 10): v1.1.0

| Elo | Evidência |
|---|---|
| Release v1.1.0 | [releases/tag/v1.1.0](https://github.com/arthurfaust/fundscope/releases/tag/v1.1.0), criada por `github-actions[bot]` em 25/11/2026 00:19 UTC |
| Commit da tag | [`3bd0884`](https://github.com/arthurfaust/fundscope/commit/3bd0884) `feat(pipeline): informa registros descartados na transformacao (#22)` (tag anotada pelo pipeline) |
| Pull Request que gerou o commit | [#22](https://github.com/arthurfaust/fundscope/pull/22), mesclado por squash por arthurfaust em 25/11/2026 00:17 UTC |
| Revisão e aprovação do par | [aprovado por mariagranza](https://github.com/arthurfaust/fundscope/pull/22#pullrequestreview-6049574034) em 25/11/2026 00:17 UTC |
| Execução do CI que liberou o merge | [`ci-ok`](https://github.com/arthurfaust/fundscope/actions/runs/45516322653/job/138876937352), [Qualidade e testes](https://github.com/arthurfaust/fundscope/actions/runs/45516322653/job/138876558965), [SCA](https://github.com/arthurfaust/fundscope/actions/runs/45516322653/job/138876558365) e [`titulo-pr`](https://github.com/arthurfaust/fundscope/actions/runs/45516322670/job/138876558103), todos verdes |
| Issue de origem | [#21: feat: informar registros descartados no pipeline](https://github.com/arthurfaust/fundscope/issues/21), fechada pelo `Closes #21` do PR |
| Quem aprovou a produção, e quando | arthurfaust, no Environment `production`, na [execução CD #10](https://github.com/arthurfaust/fundscope/actions/runs/45516988639); job [Produção](https://github.com/arthurfaust/fundscope/actions/runs/45516988639/job/138879204504) concluído em 25/11/2026 00:19 UTC |

A cadeia da v1.1.0 está completa. Depois dela, a v1.1.0 foi substituída pelo
rollback para v1.0.0 e revertida pelo [PR #24](https://github.com/arthurfaust/fundscope/pull/24)
(ver `aula-3-cd.md`).

### Falhas de processo que uma auditoria encontraria

- **PRs anteriores à Aula 1 sem Issue de origem:** #4 a #10 não citam nenhuma Issue
  (só o #2 tem `Closes #1`). Foram mesclados com *merge commit*, e alguns títulos não
  refletem o tipo da mudança (ex.: #10, `fix: ajuste do cd`, era uma mudança de CI).
  Esses commits aparecem nas notas da v1.0.0 como `Merge pull request #...`.
- **PR #24 (revert) com `Closes #<issue>` sem o número:** a Issue #23 não fechou
  automaticamente e foi fechada à mão.
- **PRs do Dependabot sem Issue de origem:** comportamento esperado da ferramenta;
  a justificativa fica no comentário de revisão de cada PR.
- **Aprovação do #29 feita pelo próprio desenvolvedor líder:** permitida, porque o
  autor é o `dependabot[bot]`, mas sem a revisão do par.
