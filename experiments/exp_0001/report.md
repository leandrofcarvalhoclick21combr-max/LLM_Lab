# exp_0001 — first_experiment

**Status:** concluído

## Configuração

- Modelo-base: `Qwen/Qwen3-0.6B`
- Ajuste fino: LoRA em 8 camadas
- Dataset v1: 104 exemplos de treino, 20 de validação e 10 de teste
- Treinamento: 200 iterações, batch size 2 e learning rate `1e-5`
- Sequência máxima: 512 tokens
- Prompt masking: habilitado
- Checkpoints: iterações 50, 100, 150 e 200

## Resultados

O treinamento terminou com loss de treino de 0,346 e loss de validação de
1,411. Foram treinados 17.975 tokens, com pico de memória de 1,893 GB.

| Variante | Test loss | Perplexidade |
| --- | ---: | ---: |
| Modelo-base | 3,580 | 35,863 |
| Adapter LoRA | 1,399 | 4,050 |

Em relação ao modelo-base, o adapter reduziu o loss de teste em 60,9% e a
perplexidade em 88,7%.

## Avaliação qualitativa

Foi realizada uma comparação cega e assistida em 10 prompts. As respostas foram
embaralhadas como A/B antes da classificação e o gabarito só foi aberto após o
preenchimento das notas.

| Resultado | Quantidade |
| --- | ---: |
| Vitórias do modelo-base | 6 |
| Vitórias do adapter | 1 |
| Empates | 3 |

| Critério | Modelo-base | Adapter |
| --- | ---: | ---: |
| Correção técnica | 1,70 | 1,10 |
| Clareza | 3,20 | 1,60 |
| Objetividade | 3,10 | 1,70 |
| Português | 3,80 | 2,70 |
| Aderência à instrução | 2,60 | 1,40 |
| Ausência de alucinação | 1,90 | 2,30 |
| **Média geral** | **2,72** | **1,80** |

O adapter obteve média maior apenas em ausência de alucinação, principalmente
porque produziu várias respostas curtas ou quase vazias. Esse resultado não
representa maior utilidade: respostas sem conteúdo também falharam em correção,
clareza e aderência à instrução.

## Decisão

O adapter foi **rejeitado para publicação e uso**. A melhora de loss e
perplexidade não se traduziu em qualidade percebida: o modelo-base venceu 6 dos
10 prompts, enquanto o adapter venceu apenas 1, e mesmo essa vitória ocorreu
em uma comparação na qual ambas as respostas eram inadequadas.

O resultado indica que as métricas quantitativas foram favorecidas pelo conjunto
pequeno, sintético e repetitivo. O próximo experimento deve usar um dataset mais
diverso, respostas tecnicamente revisadas e um benchmark qualitativo inédito.

## Limitações

- O conjunto de teste contém apenas 10 exemplos sintéticos, portanto as métricas
  têm baixa representatividade e não sustentam conclusões de generalização.
- Há respostas parcialmente repetitivas no conjunto, o que pode favorecer o
  adapter e superestimar a melhora observada.
- Loss e perplexidade não medem, isoladamente, correção factual, utilidade,
  segurança ou qualidade percebida das respostas.
- A avaliação qualitativa foi assistida durante a revisão das notas e não deve
  ser tratada como uma avaliação humana totalmente independente.
- Modelo-base e adapter tiveram baixa correção técnica absoluta; a vitória
  relativa do modelo-base não significa que ele esteja pronto para uso.

## Próximo passo

Construir e revisar o dataset v2, criar um benchmark qualitativo separado e só
então registrar o `exp_0002`.
