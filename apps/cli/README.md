# CLI

Futura interface de linha de comando do LLM Lab.

Uso inicial:

```bash
llm-lab validate configs/default.yaml
llm-lab run configs/default.yaml --dry-run
llm-lab run configs/default.yaml
llm-lab train configs/default.yaml
llm-lab train configs/default.yaml --execute
```

O comando valida os três splits antes de registrar um experimento. Nesta versão,
o runner registra configuração e metadados, mas ainda não executa o backend de
fine-tuning.

O comando `train` apenas mostra o comando MLX-LM por padrão. A opção `--execute`
é obrigatória para baixar o modelo e iniciar o uso intensivo de recursos.
