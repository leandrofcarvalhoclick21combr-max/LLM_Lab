# Datasets

## Estrutura

```text
datasets/
├── registry/
├── templates/
└── versions/
```

Cada versão deve conter, no mínimo:

```text
v1/
├── train.jsonl
├── valid.jsonl
├── test.jsonl
└── dataset.yaml
```

Os conjuntos de teste não devem ser usados no treinamento.
