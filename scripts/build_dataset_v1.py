#!/usr/bin/env python3
"""Gera o dataset sintético v1 de forma determinística."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "datasets" / "versions" / "v1"
SYSTEM = "Você é um assistente didático sobre inteligência artificial e LLMs. Responda em português do Brasil, com clareza, precisão e sem inventar fatos."

TRAIN = [
    ("token", "Token é uma unidade de texto processada pelo modelo; pode ser uma palavra, parte dela ou um sinal."),
    ("tokenizador", "Tokenizador é o componente que converte texto em IDs de tokens e faz a conversão inversa."),
    ("embedding", "Embedding é uma representação vetorial aprendida que aproxima itens com significado ou uso semelhante."),
    ("codificação posicional", "Codificação posicional fornece ao Transformer informação sobre a ordem dos tokens."),
    ("Transformer", "Transformer é uma arquitetura neural baseada em atenção, adequada ao processamento paralelo de sequências."),
    ("atenção", "Atenção pondera quais partes da entrada são mais relevantes para produzir cada representação."),
    ("self-attention", "Self-attention relaciona cada token com outros tokens da mesma sequência."),
    ("atenção multi-head", "Atenção multi-head executa vários mecanismos de atenção para capturar relações diferentes."),
    ("encoder", "Encoder transforma a entrada em representações contextuais usadas por outras partes do modelo."),
    ("decoder", "Decoder produz a saída passo a passo condicionado ao contexto e aos tokens anteriores."),
    ("modelo autorregressivo", "Modelo autorregressivo prevê o próximo token a partir dos tokens anteriores."),
    ("pré-treinamento", "Pré-treinamento aprende padrões gerais em grandes coleções de dados antes da especialização."),
    ("fine-tuning", "Fine-tuning ajusta um modelo pré-treinado com dados de uma tarefa ou domínio específico."),
    ("instruction tuning", "Instruction tuning treina o modelo com pares de instruções e respostas desejadas."),
    ("LoRA", "LoRA adapta um modelo treinando matrizes pequenas de baixa dimensão, mantendo os pesos-base congelados."),
    ("quantização", "Quantização reduz a precisão numérica dos pesos ou ativações para economizar memória e computação."),
    ("destilação", "Destilação treina um modelo menor para reproduzir comportamentos úteis de um modelo maior."),
    ("janela de contexto", "Janela de contexto é o limite de tokens que o modelo considera em uma execução."),
    ("prompt", "Prompt é a entrada que fornece instruções, contexto e dados para orientar a resposta do modelo."),
    ("system prompt", "System prompt define regras gerais e prioridades de comportamento para a interação."),
    ("temperatura", "Temperatura controla a dispersão da amostragem; valores menores tendem a respostas mais previsíveis."),
    ("top-p", "Top-p restringe a amostragem ao menor conjunto de tokens cuja probabilidade acumulada atinge um limite."),
    ("max tokens", "Max tokens limita quantos tokens novos podem ser gerados na resposta."),
    ("alucinação", "Alucinação é uma afirmação produzida sem suporte confiável nos dados ou no contexto disponível."),
    ("grounding", "Grounding ancora a resposta em fontes ou dados verificáveis fornecidos ao sistema."),
    ("RAG", "RAG combina recuperação de documentos com geração para responder usando contexto externo relevante."),
    ("banco vetorial", "Banco vetorial armazena embeddings e permite buscar itens por proximidade semântica."),
    ("similaridade de cosseno", "Similaridade de cosseno mede o alinhamento entre vetores, desconsiderando sua magnitude."),
    ("chunking", "Chunking divide documentos em trechos adequados à indexação e recuperação."),
    ("recuperação", "Recuperação seleciona informações potencialmente relevantes para uma consulta."),
    ("reranking", "Reranking reordena resultados recuperados usando um critério de relevância mais preciso."),
    ("evals", "Evals são avaliações sistemáticas que medem comportamentos e qualidade sob critérios definidos."),
    ("benchmark", "Benchmark é um conjunto padronizado de casos e métricas usado para comparar sistemas."),
    ("split de treino", "O split de treino contém exemplos usados para atualizar os parâmetros do modelo."),
    ("split de validação", "O split de validação orienta decisões durante o desenvolvimento sem treinar nos casos de teste."),
    ("split de teste", "O split de teste mede o resultado final e deve permanecer isolado do treinamento."),
    ("overfitting", "Overfitting ocorre quando o modelo memoriza padrões do treino e generaliza mal para novos dados."),
    ("underfitting", "Underfitting ocorre quando o modelo não aprende suficientemente nem mesmo os padrões do treino."),
    ("descida do gradiente", "Descida do gradiente atualiza parâmetros na direção que reduz a função de perda."),
    ("taxa de aprendizado", "Taxa de aprendizado controla o tamanho dos passos de atualização dos parâmetros."),
    ("batch", "Batch é o conjunto de exemplos processado antes de uma atualização dos parâmetros."),
    ("época", "Época corresponde a uma passagem completa pelo conjunto de treinamento."),
    ("função de perda", "Função de perda quantifica a diferença entre a previsão do modelo e o alvo esperado."),
    ("checkpoint", "Checkpoint registra um estado do treinamento para avaliação, retomada ou publicação."),
    ("seed", "Seed inicializa geradores pseudoaleatórios e ajuda a reproduzir um experimento."),
    ("reprodutibilidade", "Reprodutibilidade é a capacidade de repetir um experimento sob condições registradas."),
    ("GPU", "GPU acelera operações matriciais paralelas comuns no treinamento e na inferência neural."),
    ("VRAM", "VRAM é a memória da GPU usada por pesos, ativações, gradientes e caches."),
    ("inferência", "Inferência é o uso de um modelo treinado para produzir previsões ou respostas."),
    ("latência", "Latência é o tempo entre uma solicitação e a entrega da resposta ou de seu primeiro token."),
    ("throughput", "Throughput mede a quantidade de requisições ou tokens processados por unidade de tempo."),
    ("streaming", "Streaming entrega partes da resposta à medida que são geradas."),
]

VALID = [
    ("perplexidade", "Perplexidade deriva da perda probabilística e indica quão surpreendente um texto é para o modelo."),
    ("entropia cruzada", "Entropia cruzada penaliza a diferença entre a distribuição prevista e o alvo correto."),
    ("masking", "Masking impede que certas posições participem da atenção ou da perda conforme o objetivo do treino."),
    ("padding", "Padding completa sequências com tokens especiais para permitir processamento em lotes uniformes."),
    ("token EOS", "EOS sinaliza o fim de uma sequência para o tokenizador e o modelo."),
    ("token BOS", "BOS sinaliza o início de uma sequência quando o template do modelo o utiliza."),
    ("function calling", "Function calling permite ao modelo produzir argumentos estruturados para uma função disponível."),
    ("agente", "Agente combina um modelo com estado, ferramentas e um ciclo de decisão orientado a objetivos."),
    ("ferramenta", "Ferramenta é uma capacidade externa invocada pelo modelo para consultar dados ou executar ações."),
    ("guardrail", "Guardrail é um controle que valida, restringe ou monitora entradas, decisões e saídas do sistema."),
]

TEST = [
    ("RLHF", "RLHF usa preferências humanas e aprendizado por reforço para alinhar o comportamento do modelo."),
    ("DPO", "DPO otimiza diretamente preferências entre respostas sem treinar explicitamente um modelo de recompensa."),
    ("Mixture of Experts", "Mixture of Experts encaminha cada token a uma parte selecionada dos especialistas do modelo."),
    ("KV cache", "KV cache reutiliza chaves e valores da atenção de tokens anteriores para acelerar a geração."),
    ("decodificação especulativa", "Decodificação especulativa usa um modelo auxiliar para propor tokens verificados pelo modelo principal."),
]


def examples(items: list[tuple[str, str]]) -> list[dict[str, object]]:
    rows = []
    for term, definition in items:
        rows.append({"messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": f"Explique o que é {term}."}, {"role": "assistant", "content": definition}]})
        practical = (
            f"Em um projeto de LLM, considere o seguinte: {definition} "
            "A aplicação concreta deve ser validada com métricas adequadas ao objetivo do sistema."
        )
        rows.append({"messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": f"Como o conceito de {term} aparece em um projeto de LLM?"}, {"role": "assistant", "content": practical}]})
    return rows


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    splits = {"train": examples(TRAIN), "valid": examples(VALID), "test": examples(TEST)}
    for name, rows in splits.items():
        path = OUTPUT / f"{name}.jsonl"
        text = "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows)
        path.write_text(text, encoding="utf-8")
        print(f"{name}: {len(rows)} registros sha256={hashlib.sha256(text.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
