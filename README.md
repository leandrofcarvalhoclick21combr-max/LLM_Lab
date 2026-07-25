# LLM Lab

**Versão:** 0.1.0-alpha  
**Status:** Alpha  
**Criado em:** 2026-07-14 23:30:58

## Missão

O LLM Lab é uma plataforma de engenharia para criar, treinar, avaliar, versionar e publicar modelos de linguagem especializados para diferentes domínios empresariais.

## Objetivo inicial

A primeira fase transforma experimentos manuais em um processo reproduzível:

1. registrar datasets;
2. registrar configurações;
3. executar fine-tuning;
4. avaliar modelo-base e modelo ajustado;
5. gerar relatórios;
6. manter histórico de experimentos.

## Estrutura

- `configs/`: configurações de treinamento e avaliação;
- `datasets/`: templates, versões e registro de datasets;
- `models/`: modelos-base, adaptadores e modelos publicados;
- `experiments/`: histórico de experimentos reproduzíveis;
- `benchmarks/`: conjuntos e rotinas de avaliação;
- `reports/`: relatórios consolidados;
- `pipelines/`: orquestração de treinamento e avaliação;
- `apps/`: futuras interfaces CLI, API e web;
- `deployment/`: empacotamento e implantação;
- `tests/`: testes automatizados.

## Primeiro componente

O primeiro componente oficial será o **Experiment Runner**, responsável por ler uma configuração, criar um experimento, executar as etapas e registrar os resultados.

## Desenvolvimento local

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
```

Antes de registrar um experimento, crie os arquivos indicados em
`configs/default.yaml` e valide o fluxo:

```bash
llm-lab validate configs/default.yaml
llm-lab run configs/default.yaml --dry-run
```

## Avaliação qualitativa cega

Depois de treinar um adapter, gere respostas A/B embaralhadas com:

```bash
python -m pip install -e '.[dev,train]'
llm-lab evaluate-qualitative exp_0001
```

O comando usa os prompts de teste registrados no experimento e cria:

- `experiments/exp_0001/results/qualitative/review.md`: formulário para avaliação;
- `experiments/exp_0001/results/qualitative/answer_key.json`: identificação dos modelos,
  que só deve ser aberta depois de preencher o formulário.
