# CLI

Futura interface de linha de comando do LLM Lab.

Uso inicial:

```bash
llm-lab validate configs/default.yaml
llm-lab run configs/default.yaml --dry-run
llm-lab run configs/default.yaml
```

O comando valida os três splits antes de registrar um experimento. Nesta versão,
o runner registra configuração e metadados, mas ainda não executa o backend de
fine-tuning.
