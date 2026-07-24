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

## Reconstrução do v1

O dataset sintético inicial é gerado de forma determinística:

```bash
python scripts/build_dataset_v1.py
llm-lab validate configs/default.yaml
```

Os arquivos JSONL permanecem locais; o gerador, o manifesto com hashes e o
registro são versionados. O `v1` exige revisão humana antes de treinamento.
