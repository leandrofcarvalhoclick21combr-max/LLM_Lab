# Diário do projeto LLM Lab

Este documento registra a evolução técnica do LLM Lab, as decisões tomadas e
os aprendizados obtidos. Ele complementa o `CHANGELOG.md`: enquanto o changelog
lista mudanças de produto, este diário preserva o contexto e o raciocínio por
trás de cada etapa.

## Visão geral

O LLM Lab nasceu para transformar experimentos manuais com modelos de linguagem
em um processo reproduzível. O fluxo adotado é:

```text
configuração → dataset → experimento → treinamento → avaliação → decisão
```

Até aqui, construímos a fundação do laboratório, executamos o primeiro
fine-tuning LoRA, confrontamos métricas automáticas com avaliação humana e
decidimos não publicar um adapter que parecia bom quantitativamente, mas falhou
qualitativamente.

## Linha do tempo

### 14 de julho de 2026 — Fundação do projeto

O repositório foi criado como `LLM Lab 0.1.0-alpha`, com:

- missão, arquitetura, roadmap e changelog;
- diretórios para configurações, datasets, modelos, experimentos e aplicações;
- separação entre modelos-base, adapters experimentais e modelos publicados;
- princípio de que todo treinamento deve pertencer a um experimento registrado.

Marco: commit inicial `8d95e4a`.

### 24 de julho de 2026 — Experiment Runner mínimo

Foi implementado o primeiro fluxo reproduzível do projeto:

- carregamento e validação de configurações YAML;
- validação estrutural de datasets conversacionais em JSONL;
- criação de manifestos e relatórios de experimentos;
- registro central em `experiments/index.yaml`;
- comandos de CLI para validação e execução em modo seguro;
- testes unitários, teste de integração e CI com `pytest`.

Marco: [PR #1](https://github.com/leandrofcarvalhoclick21combr-max/LLM_Lab/pull/1).

### 24 de julho de 2026 — Dataset v1

O primeiro dataset sintético foi reconstruído e revisado:

- 104 registros de treino;
- 20 registros de validação;
- 10 registros de teste;
- idioma `pt-BR`;
- domínio de inteligência artificial e LLMs;
- conceitos separados entre os splits;
- hashes e quantidades registrados no manifesto;
- revisão humana obrigatória e aprovação explícita.

O conteúdo dos JSONL permaneceu fora do Git por política de dados, enquanto o
manifesto `dataset.yaml` foi versionado.

Marco: [PR #2](https://github.com/leandrofcarvalhoclick21combr-max/LLM_Lab/pull/2).

### 25 de julho de 2026 — Registro do exp_0001

O primeiro experimento foi registrado com a seguinte configuração:

| Parâmetro | Valor |
| --- | --- |
| Modelo-base | `Qwen/Qwen3-0.6B` |
| Técnica | LoRA |
| Iterações | 200 |
| Batch size | 2 |
| Camadas ajustadas | 8 |
| Learning rate | `1e-5` |
| Sequência máxima | 512 tokens |
| Prompt masking | habilitado |
| Checkpoints | a cada 50 iterações |

O manifesto também vinculou o experimento ao dataset v1 e tornou explícita a
necessidade de avaliação humana.

Marco: [PR #3](https://github.com/leandrofcarvalhoclick21combr-max/LLM_Lab/pull/3).

### 25 de julho de 2026 — Backend seguro de treinamento MLX

Foi incorporado um backend de treinamento LoRA com MLX que:

- exige macOS com Apple Silicon;
- verifica a presença do backend antes da execução;
- rejeita datasets ainda não aprovados;
- impede sobrescrever silenciosamente um diretório de adapter existente;
- constrói o comando de treinamento a partir da configuração registrada;
- mantém adapters, checkpoints e logs fora do controle de versão.

Marco: [PR #4](https://github.com/leandrofcarvalhoclick21combr-max/LLM_Lab/pull/4).

### 25 de julho de 2026 — Treinamento e avaliação quantitativa

O `exp_0001` foi treinado até a iteração 200. Foram preservados localmente o
adapter final e os checkpoints das iterações 50, 100, 150 e 200.

Resultados de treinamento:

| Métrica | Resultado |
| --- | ---: |
| Train loss final | 0,346 |
| Validation loss final | 1,411 |
| Tokens treinados | 17.975 |
| Pico de memória | 1,893 GB |

Resultados no conjunto de teste:

| Variante | Test loss | Perplexidade |
| --- | ---: | ---: |
| Modelo-base | 3,580 | 35,863 |
| Adapter LoRA | 1,399 | 4,050 |

O adapter reduziu o loss em aproximadamente 60,9% e a perplexidade em 88,7%.
Esses números justificaram avançar para avaliação qualitativa, mas não aprovaram
o modelo para publicação.

### 25 de julho de 2026 — Avaliação qualitativa cega

Foi criado o comando:

```bash
llm-lab evaluate-qualitative exp_0001
```

O avaliador:

- lê os prompts de teste registrados no experimento;
- gera respostas do modelo-base e do adapter com os mesmos parâmetros;
- embaralha cada par como resposta A/B;
- cria um formulário Markdown para classificação;
- mantém o gabarito separado até o fim da avaliação.

Durante a primeira execução, o Qwen3 expôs blocos internos `<think>` em inglês.
Esse raciocínio consumiu o limite de tokens e cortou respostas finais. O gerador
foi corrigido para desabilitar o modo de raciocínio, exigir somente a resposta
final em português e remover preventivamente tags internas residuais.

Marco: [PR #5](https://github.com/leandrofcarvalhoclick21combr-max/LLM_Lab/pull/5).

### 26 de julho de 2026 — Resultado qualitativo e decisão

A comparação foi feita às cegas em 10 prompts. As notas foram posteriormente
revisadas de forma assistida para corrigir casos em que a resposta relativamente
melhor havia recebido nota alta apesar de continuar factualmente errada.

Resultado de preferência:

| Resultado | Quantidade |
| --- | ---: |
| Vitórias do modelo-base | 6 |
| Vitórias do adapter | 1 |
| Empates | 3 |

Resultado médio por critério:

| Critério | Modelo-base | Adapter |
| --- | ---: | ---: |
| Correção técnica | 1,70 | 1,10 |
| Clareza | 3,20 | 1,60 |
| Objetividade | 3,10 | 1,70 |
| Português | 3,80 | 2,70 |
| Aderência à instrução | 2,60 | 1,40 |
| Ausência de alucinação | 1,90 | 2,30 |
| **Média geral** | **2,72** | **1,80** |

O adapter apareceu ligeiramente melhor em ausência de alucinação porque produziu
respostas curtas ou quase vazias. Isso não representou maior qualidade: as mesmas
respostas falharam em correção, clareza e aderência.

Decisão final: **o adapter do exp_0001 foi rejeitado para publicação e uso**.

Marco: [PR #6](https://github.com/leandrofcarvalhoclick21combr-max/LLM_Lab/pull/6).

## O que construímos até aqui

- uma estrutura de projeto orientada a experimentos reproduzíveis;
- validação automática de configurações e datasets JSONL;
- registro central e manifestos por experimento;
- backend LoRA com MLX e verificações de segurança;
- geração de checkpoints e preservação local de artefatos pesados;
- avaliação quantitativa de modelo-base e adapter;
- avaliação qualitativa cega com formulário e gabarito;
- registro estruturado de métricas e decisões;
- testes automatizados e workflow de CI;
- uma política prática: métricas melhores não substituem avaliação humana.

## Principais aprendizados

1. Loss e perplexidade podem melhorar sem que a resposta fique mais útil ou
   correta.
2. Um conjunto de teste pequeno, sintético e repetitivo pode superestimar o
   desempenho do adapter.
3. Respostas curtas podem parecer menos alucinatórias, mas ainda serem inúteis.
4. Avaliações relativas precisam manter uma escala absoluta: a resposta vencedora
   ainda pode ser ruim.
5. O benchmark deve ficar isolado do treinamento e conter formulações realmente
   inéditas.
6. Artefatos pesados e logs devem permanecer locais; manifestos, resultados e
   decisões devem ser versionados.
7. Um resultado negativo bem documentado é um resultado útil: ele impede a
   publicação de um modelo inadequado e orienta o próximo experimento.

## Estado atual

- `exp_0001`: concluído;
- adapter: rejeitado para publicação e uso;
- avaliação quantitativa: concluída;
- avaliação qualitativa cega e assistida: concluída;
- suíte automatizada: 14 testes;
- próximo experimento: ainda não registrado;
- próximo marco: dataset v2.

## Próxima etapa — dataset v2

Antes do `exp_0002`, o dataset v2 deverá:

- aumentar a diversidade de conceitos, perguntas e estilos de resposta;
- remover frases-modelo repetitivas;
- usar respostas completas e tecnicamente revisadas;
- incluir exemplos negativos e distinções entre conceitos semelhantes;
- manter treino, validação e teste semanticamente separados;
- criar um benchmark qualitativo inédito, fora do treinamento;
- passar por revisão humana antes de ser aprovado.

O objetivo do próximo ciclo não será apenas reduzir loss, mas demonstrar melhora
simultânea em correção, clareza, aderência e preferência humana.

## Como manter este diário

A cada marco relevante, adicionar uma entrada com:

1. data e objetivo;
2. o que foi construído ou alterado;
3. configuração e métricas relevantes;
4. problemas encontrados;
5. decisão tomada;
6. link para o PR ou experimento;
7. próximo passo.
