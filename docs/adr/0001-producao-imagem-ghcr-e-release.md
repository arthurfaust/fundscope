# 0001: Produção é a imagem no GHCR mais a Release do GitHub

- Status: aceito
- Data: 24/11/2026

## Contexto

O modelo de CD da disciplina (Aula 3) gera um pacote `.zip` e trata a Release do
GitHub como "produção". O FundScope, porém, é um pipeline de dados em Python que roda
em container: o que de fato executa é a imagem Docker, e não há servidor de
hospedagem gratuito disponível para manter um ambiente de produção no ar.

Restrições: conta GitHub pessoal no plano gratuito, repositório público, rede do
laboratório restrita e nenhum serviço de nuvem além do GitHub.

## Decisão

A produção do FundScope é a combinação de dois itens:

- **Imagem Docker** `ghcr.io/arthurfaust/fundscope`, publicada no GitHub Container
  Registry. A imagem é construída **uma única vez** por merge, com a tag
  `sha-<commit>`; staging e produção apenas acrescentam tags à mesma imagem
  (`docker buildx imagetools create`), sem reconstruir.
- **Release do GitHub** `vX.Y.Z`, criada pelo pipeline após a aprovação no
  Environment `production`, com notas geradas a partir dos títulos dos PRs e o
  código-fonte da versão anexado.

As tags da imagem têm papéis fixos:

| Tag | Significado |
|---|---|
| `sha-<commit>` | candidata, construída no job `preparar` |
| `staging` | última candidata executada com sucesso em staging |
| `vX.Y.Z` | baseline aprovada, imutável |
| `production` e `latest` | versão oficial em uso |

O rollback (`rollback.yml`) reaponta `production` e `latest` para a imagem de uma
`vX.Y.Z` anterior e marca a Release dela como *Latest*, também sem recompilar.

## Alternativas consideradas

- **Somente o `.zip` do modelo da aula:** atende à forma da aula, mas o pacote
  não é o que executa; a versão aprovada não corresponderia ao artefato real.
- **Reconstruir a imagem no job de produção:** mais simples de escrever, mas a
  imagem publicada não seria a mesma testada em staging (imagem base, dependências
  ou a `main` podem mudar entre os dois builds), o que viola o PGC 6.
- **Hospedar o pipeline em um serviço de nuvem (Render, Railway, Fly.io):** daria
  um ambiente executando de verdade, mas exige conta, cartão ou token extra e
  depende de domínios que a rede do laboratório pode bloquear. Fica como evolução.

## Consequências

- A versão aprovada é exatamente a imagem testada em staging, rastreável pelo
  commit (`sha-<commit>`) e pela versão (`vX.Y.Z`).
- O rollback é imediato e não depende de build.
- Não existe um ambiente "rodando": produção significa "imagem oficial pronta para
  ser executada". Quem opera o pipeline precisa usar a tag `production`.
- As imagens se acumulam no GHCR, uma por merge. Uma política de limpeza das tags
  `sha-*` antigas fica pendente.
- Atualizações de dependência com título `chore(deps)` não geram versão: só chegam
  à produção no próximo `feat` ou `fix` (ver ADR 0002).
