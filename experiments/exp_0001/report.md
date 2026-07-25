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

## Decisão

O adapter apresentou melhora quantitativa suficiente para avançar à avaliação
qualitativa comparativa com o modelo-base. O experimento de treinamento está
concluído, mas o adapter ainda não está aprovado para publicação ou uso: a
avaliação humana permanece pendente.

## Limitações

- O conjunto de teste contém apenas 10 exemplos sintéticos, portanto as métricas
  têm baixa representatividade e não sustentam conclusões de generalização.
- Há respostas parcialmente repetitivas no conjunto, o que pode favorecer o
  adapter e superestimar a melhora observada.
- Loss e perplexidade não medem, isoladamente, correção factual, utilidade,
  segurança ou qualidade percebida das respostas.
- Ainda não foi realizada uma comparação humana, lado a lado e às cegas, entre
  o modelo-base e o adapter.

## Próximo passo

Executar a avaliação qualitativa do modelo-base e do adapter nos mesmos prompts,
registrando preferência, correção, relevância e sinais de memorização ou
repetição.
