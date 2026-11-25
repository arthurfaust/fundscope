# Evidências: Aula 3, Entrega Contínua

Seções do PGC aplicadas: 3.3 (SemVer), 6.1 (CD e gates), 6.4 (rollback) e 9 (baselines e releases).

## Adaptação do modelo ao FundScope

O modelo da aula gera um pacote `.zip`; no FundScope o artefato de produção é a imagem
Docker no GHCR. Os princípios do PGC foram mantidos:

| PGC | No FundScope |
|---|---|
| Build único promovido entre ambientes | imagem construída uma vez como `sha-<commit>`; staging e produção só adicionam tags (`docker buildx imagetools create`) |
| Staging | execução da imagem candidata e tag `staging` |
| Gate de aprovação | Environment `production` com revisor obrigatório |
| Baseline | imagem `vX.Y.Z` + tag Git `vX.Y.Z` + Release com notas e código-fonte anexado |
| Rollback | reaponta `production` e `latest` para a imagem da versão escolhida e marca a Release como *Latest*, sem recompilar |

## Rastreabilidade da implantação

| Item | Link |
|---|---|
| Issue de origem | [#17: ci: configurar entrega continua conforme Aula 3](https://github.com/arthurfaust/fundscope/issues/17) |
| Pull request do CD | [#18](https://github.com/arthurfaust/fundscope/pull/18) → commit [`933e0ae`](https://github.com/arthurfaust/fundscope/commit/933e0ae) |
| Arquivos | `.github/workflows/cd.yml`, `.github/workflows/rollback.yml`, `scripts/proxima-versao.mjs` |

## Baselines geradas

| Versão | PR (título) | Issue | Release | Execução do CD | Aprovação da produção |
|---|---|---|---|---|---|
| v1.0.0 | primeiro merge sem tag ([#18](https://github.com/arthurfaust/fundscope/pull/18)) | [#17](https://github.com/arthurfaust/fundscope/issues/17) | [v1.0.0](https://github.com/arthurfaust/fundscope/releases/tag/v1.0.0) | [CD #8](https://github.com/arthurfaust/fundscope/actions/runs/44915788072) | arthurfaust, 24/11/2026 |
| v1.0.1 | `fix(transform): descarta registros com CNPJ invalido` ([#20](https://github.com/arthurfaust/fundscope/pull/20)) | [#19](https://github.com/arthurfaust/fundscope/issues/19) | [v1.0.1](https://github.com/arthurfaust/fundscope/releases/tag/v1.0.1) | [CD #9](https://github.com/arthurfaust/fundscope/actions/runs/45515039070) | arthurfaust, 25/11/2026 |
| v1.1.0 | `feat(pipeline): informa registros descartados na transformacao` ([#22](https://github.com/arthurfaust/fundscope/pull/22)) | [#21](https://github.com/arthurfaust/fundscope/issues/21) | [v1.1.0](https://github.com/arthurfaust/fundscope/releases/tag/v1.1.0) | [CD #10](https://github.com/arthurfaust/fundscope/actions/runs/45516988639) | arthurfaust, 25/11/2026 |

As notas de cada Release separam *Funcionalidades*, *Correções* e *Outros*:
a v1.0.1 lista só a correção e a v1.1.0 só a funcionalidade.

PRs que não geram versão (`docs`, `ci`, `chore`, `test`, `revert`) rodam até staging
e o job **Produção** fica *skipped*, como no revert abaixo.

## Rollback (PGC 6.4)

| Item | Valor |
|---|---|
| Execução | [Rollback para v1.0.0](https://github.com/arthurfaust/fundscope/actions/runs/45517364944) |
| Solicitado e aprovado por | arthurfaust, com o comentário "Rollback simulado: defeito grave na v1.1.0 (Aula 3)" |
| Resultado | v1.0.0 voltou a ser a Release *Latest*; tags `production` e `latest` da imagem apontam para `v1.0.0` |

## Revert pelo fluxo normal

| Item | Link |
|---|---|
| Issue | [#23: fix: defeito simulado na v1.1.0 exige reverter a funcionalidade](https://github.com/arthurfaust/fundscope/issues/23) |
| Pull request | [#24: revert: remove informe de registros descartados (v1.1.0)](https://github.com/arthurfaust/fundscope/pull/24), aprovado por mariagranza |
| Commit na `main` | [`90ff562`](https://github.com/arthurfaust/fundscope/commit/90ff562) |
| CD após o revert | [CD #11](https://github.com/arthurfaust/fundscope/actions/runs/45518285342): staging executado, Produção *skipped* (sem versão nova) |

## Ocorrências registradas

- **Fila do CD bloqueada:** a execução [CD #7](https://github.com/arthurfaust/fundscope/actions/runs/44913777546)
  (PR `docs:` #16, ainda com o `cd.yml` antigo) ficou aguardando aprovação desde 21/11 e
  segurou a fila (`concurrency` sem cancelamento). A execução do CD novo (#8) foi cancelada
  por engano, a #7 foi encerrada sem promover a produção e a #8 foi reexecutada (tentativa 2).
- **Issue sem fechamento automático:** a descrição do PR #24 ficou com `Closes #<issue>`
  sem o número; a Issue #23 foi fechada manualmente com referência ao PR.

## Para discutir

Por que gerar o pacote uma única vez? Se staging e produção fossem compilados separadamente,
a imagem aprovada não seria a mesma publicada: uma dependência resolvida em outro momento,
uma imagem base atualizada ou uma mudança na `main` entre os dois builds poderiam colocar
em produção algo que nunca foi testado em staging.
