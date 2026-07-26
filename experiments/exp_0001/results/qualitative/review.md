# Avaliação qualitativa cega

Compare A e B sem abrir `answer_key.json`. Dê notas de 1 (ruim) a 5 (excelente).
Em alucinação, use 1 para muita invenção e 5 para nenhuma invenção.

## Prompt 1

Explique o que é RLHF.

### Resposta A

RLHF

### Resposta B

RLHF é uma abreviação para **Reinforcement Learning with Guidance**, que refere-se a um método de treinamento de modelos de inteligência artificial que ajuda a evitar comportamentos adversos ou maliciosos.

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 1 | 1 |
| Clareza | 1 | 3 |
| Objetividade | 1 | 3 |
| Português | 1 | 4 |
| Aderência à instrução | 1 | 2 |
| Ausência de alucinação | 1 | 1 |

**Vencedor (A/B/empate):** B

**Observações:** B é mais informativa, mas expande RLHF incorretamente como “Reinforcement Learning with Guidance”. A não apresenta uma explicação.

## Prompt 2

Como o conceito de RLHF aparece em um projeto de LLM?

### Resposta A

O conceito de RLHF (Reasoning and Language for Human Evaluation) aparece em projetos de LLM (Large Language Models) para garantir que os modelos sejam avaliados com base em razões e em lógica, evitando falhas ou comportamentos inapropriados.

### Resposta B

Em um projeto de LLM

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 1 | 1 |
| Clareza | 3 | 1 |
| Objetividade | 3 | 1 |
| Português | 4 | 2 |
| Aderência à instrução | 2 | 1 |
| Ausência de alucinação | 1 | 3 |

**Vencedor (A/B/empate):** empate

**Observações:** A inventa a expansão de RLHF e descreve o conceito incorretamente. B não inventa uma definição, mas está incompleta. Nenhuma é utilizável.

## Prompt 3

Explique o que é DPO.

### Resposta A

DPO é um modelo de inteligência artificial que utiliza uma rede neural para prever o comportamento humano.

### Resposta B

DPO adapta a resposta ao contexto.

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 1 | 1 |
| Clareza | 3 | 2 |
| Objetividade | 3 | 2 |
| Português | 4 | 4 |
| Aderência à instrução | 2 | 1 |
| Ausência de alucinação | 1 | 2 |

**Vencedor (A/B/empate):** B

**Observações:** Nenhuma resposta define Direct Preference Optimization. B é menos específica e, portanto, ligeiramente menos enganosa, mas continua inadequada.

## Prompt 4

Como o conceito de DPO aparece em um projeto de LLM?

### Resposta A

Em um projeto de LLM.

### Resposta B

O conceito de DPO (Distributed Progressive Optimization) aparece em um projeto de LLM (Large Language Model) como parte de técnicas de treinamento que permitem otimizar a percepção do modelo em etapas progressivas, aumentando a eficiência e a qualidade do aprendizado.

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 1 | 1 |
| Clareza | 1 | 4 |
| Objetividade | 1 | 3 |
| Português | 3 | 4 |
| Aderência à instrução | 1 | 2 |
| Ausência de alucinação | 3 | 1 |

**Vencedor (A/B/empate):** B

**Observações:** A não responde à pergunta. B é mais completa, mas inventa “Distributed Progressive Optimization” e descreve um processo incorreto.

## Prompt 5

Explique o que é Mixture of Experts.

### Resposta A

O Mixture of Experts é uma técnica de inteligência artificial que combina múltiplos modelos de experts, cada um especializado em um conjunto de tópicos ou habilidades específicas. Esses modelos são combinados para produzir uma resposta mais completa e diversificada.

### Resposta B

Mixture of Experts

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 3 | 1 |
| Clareza | 4 | 1 |
| Objetividade | 4 | 1 |
| Português | 3 | 2 |
| Aderência à instrução | 4 | 1 |
| Ausência de alucinação | 3 | 3 |

**Vencedor (A/B/empate):** A

**Observações:** A apresenta a ideia geral de múltiplos especialistas, embora simplifique o mecanismo de roteamento. B apenas repete o termo e não explica o conceito.

## Prompt 6

Como o conceito de Mixture of Experts aparece em um projeto de LLM?

### Resposta A

O conceito de Mixture of Experts aparece em projetos de LLM, como o modelo de resposta de múltiplas experts (Mixture of Experts).

### Resposta B

Em um projeto de LLM, considere o seguinte: Mixture of Experts combina vários Expertise Headings com pesos. A aplicação concreta deve ser validada com métricas adequadas ao objetivo do sistema.

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 2 | 1 |
| Clareza | 2 | 2 |
| Objetividade | 2 | 2 |
| Português | 3 | 2 |
| Aderência à instrução | 2 | 2 |
| Ausência de alucinação | 2 | 1 |

**Vencedor (A/B/empate):** A

**Observações:** A é circular e superficial, mas menciona múltiplos especialistas. B inventa “Expertise Headings” e não explica corretamente o roteamento de tokens.

## Prompt 7

Explique o que é KV cache.

### Resposta A

O KV Cache é um cache de dados que armazena informações para melhorar a performance do modelo de inteligência artificial.

### Resposta B

KV cache

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 3 | 1 |
| Clareza | 3 | 1 |
| Objetividade | 3 | 1 |
| Português | 4 | 2 |
| Aderência à instrução | 4 | 1 |
| Ausência de alucinação | 4 | 3 |

**Vencedor (A/B/empate):** A

**Observações:** A é genérica, mas descreve parcialmente a finalidade do cache. Faltou mencionar as chaves e os valores da atenção. B não explica o conceito.

## Prompt 8

Como o conceito de KV cache aparece em um projeto de LLM?

### Resposta A

O conceito de KV cache aparece em projetos de LLM (Large Language Models) como em modelos de linguagem avançada, onde a cache é usada para armazenar e recuperar informações de um contexto anterior, otimizando o desempenho e a eficiência computacional.

### Resposta B

Em um projeto de LLM, considere o seguinte: KV cache armazena informações previamente processadas e atualizações.

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 3 | 2 |
| Clareza | 4 | 3 |
| Objetividade | 4 | 3 |
| Português | 4 | 3 |
| Aderência à instrução | 4 | 3 |
| Ausência de alucinação | 4 | 3 |

**Vencedor (A/B/empate):** A

**Observações:** A relaciona corretamente o cache com reutilização de contexto e eficiência, mas não menciona explicitamente as chaves e os valores da atenção. B é vaga.

## Prompt 9

Explique o que é decodificação especulativa.

### Resposta A

Decodificação especulativa produz a resposta para uma pergunta fornecida.

### Resposta B

Decodificação especulativa é o processo de interpretar um texto ou uma mensagem de forma a supor que o conteúdo está sendo interpretado de forma não direta, mas com base em suposições ou expectativas.

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 1 | 1 |
| Clareza | 2 | 3 |
| Objetividade | 2 | 3 |
| Português | 4 | 4 |
| Aderência à instrução | 1 | 2 |
| Ausência de alucinação | 2 | 1 |

**Vencedor (A/B/empate):** empate

**Observações:** A é vaga e não explica o mecanismo. B confunde decodificação especulativa com interpretação baseada em suposições. Nenhuma está correta.

## Prompt 10

Como o conceito de decodificação especulativa aparece em um projeto de LLM?

### Resposta A

O conceito de decodificação especulativa aparece em projetos de inteligência artificial e LLMs, onde a modelagem de linguagem é baseada em suposições ou estratégias de gerar textos com base em dados previamente explorados.

### Resposta B

Em um projeto de LLM, considere o seguinte: Decodificação especulativa produz a resposta mais provável para um token.

| Critério | A (1–5) | B (1–5) |
| --- | ---: | ---: |
| Correção técnica | 1 | 1 |
| Clareza | 3 | 2 |
| Objetividade | 3 | 3 |
| Português | 4 | 4 |
| Aderência à instrução | 2 | 2 |
| Ausência de alucinação | 1 | 2 |

**Vencedor (A/B/empate):** empate

**Observações:** A descreve incorretamente geração baseada em suposições. B também não explica o uso de um modelo auxiliar que propõe tokens verificados pelo modelo principal.
