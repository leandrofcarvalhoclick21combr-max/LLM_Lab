# Arquitetura do LLM Lab

## Princípios

1. Todo treinamento deve pertencer a um experimento registrado.
2. Todo experimento deve indicar modelo, dataset e parâmetros.
3. Datasets, adaptadores e resultados devem ser versionados.
4. Avaliação deve ser reproduzível.
5. Componentes experimentais não devem ser confundidos com componentes publicados.

## Fluxo principal

```text
Configuração
    ↓
Validação do dataset
    ↓
Criação do experimento
    ↓
Fine-tuning
    ↓
Avaliação
    ↓
Relatório
    ↓
Registro e decisão
```

## Responsabilidades

### `configs/`
Arquivos declarativos usados pelos pipelines.

### `datasets/`
Armazena versões, templates e metadados dos conjuntos de dados.

### `models/`
Armazena referências de modelos-base, adaptadores e versões publicadas.

### `experiments/`
Cada experimento deve ter configuração, logs, artefatos, resultados e decisão.

### `benchmarks/`
Contém perguntas, critérios e código de avaliação.

### `pipelines/`
Coordena as etapas de treinamento, avaliação e publicação.

### `apps/`
Interfaces para usuários e integrações.

### `deployment/`
Configuração de execução local, contêineres e nuvem.
