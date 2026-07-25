from __future__ import annotations

import gc
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yaml

from llm_lab.project import find_project_root


class QualitativeEvaluationError(RuntimeError):
    """Indica que a avaliação qualitativa não pôde ser preparada."""


@dataclass(frozen=True)
class EvaluationPrompt:
    system: str
    user: str


@dataclass(frozen=True)
class EvaluationOutput:
    review_path: Path
    answer_key_path: Path
    prompts: int


Generator = Callable[[str, str | None, list[dict[str, str]], int], str]


def run_qualitative_evaluation(
    experiment_id: str,
    *,
    seed: int = 42,
    generator: Generator | None = None,
) -> EvaluationOutput:
    root = find_project_root(Path.cwd())
    experiment_dir = root / "experiments" / experiment_id
    manifest_path = experiment_dir / "experiment.yaml"
    if not manifest_path.is_file():
        raise QualitativeEvaluationError(f"Experimento não encontrado: {experiment_id}")

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    model = manifest["model"]
    test_file = root / manifest["configuration"]["dataset"]["test_file"]
    max_tokens = int(manifest["configuration"]["evaluation"]["max_tokens"])
    adapter_path = root / manifest["configuration"]["model"]["adapter_output"] / experiment_id
    if not adapter_path.is_dir():
        raise QualitativeEvaluationError(f"Adapter não encontrado: {adapter_path}")

    prompts = load_prompts(test_file)
    if generator is None:
        print(f"Gerando {len(prompts)} respostas com o modelo-base...")
        base_responses = mlx_generate_all(model, None, prompts, max_tokens)
        print(f"Gerando {len(prompts)} respostas com o adapter...")
        adapter_responses = mlx_generate_all(model, str(adapter_path), prompts, max_tokens)
    else:
        print(f"Gerando {len(prompts)} respostas com o modelo-base...")
        base_responses = _generate_all(generator, model, None, prompts, max_tokens)
        print(f"Gerando {len(prompts)} respostas com o adapter...")
        adapter_responses = _generate_all(
            generator, model, str(adapter_path), prompts, max_tokens
        )

    assignments = blind_responses(prompts, base_responses, adapter_responses, seed=seed)
    output_dir = experiment_dir / "results" / "qualitative"
    output_dir.mkdir(parents=True, exist_ok=True)
    review_path = output_dir / "review.md"
    answer_key_path = output_dir / "answer_key.json"
    review_path.write_text(render_review(assignments), encoding="utf-8")
    answer_key_path.write_text(
        json.dumps(render_answer_key(assignments, seed), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return EvaluationOutput(review_path, answer_key_path, len(prompts))


def load_prompts(path: Path) -> list[EvaluationPrompt]:
    prompts: list[EvaluationPrompt] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            messages = row.get("messages", [])
            systems = [item["content"] for item in messages if item.get("role") == "system"]
            users = [item["content"] for item in messages if item.get("role") == "user"]
            if not users:
                raise QualitativeEvaluationError(
                    f"Prompt de usuário ausente em {path}:{line_number}"
                )
            prompts.append(EvaluationPrompt(systems[-1] if systems else "", users[-1]))
    if not prompts:
        raise QualitativeEvaluationError(f"Nenhum prompt encontrado em: {path}")
    return prompts


def _generate_all(
    generator: Generator,
    model: str,
    adapter_path: str | None,
    prompts: list[EvaluationPrompt],
    max_tokens: int,
) -> list[str]:
    responses: list[str] = []
    for index, prompt in enumerate(prompts, start=1):
        messages = []
        if prompt.system:
            messages.append({"role": "system", "content": prompt.system})
        messages.append({"role": "user", "content": prompt.user})
        print(f"  prompt {index}/{len(prompts)}")
        responses.append(generator(model, adapter_path, messages, max_tokens).strip())
    return responses


def mlx_generate_all(
    model_name: str,
    adapter_path: str | None,
    prompts: list[EvaluationPrompt],
    max_tokens: int,
) -> list[str]:
    try:
        import mlx.core as mx
        from mlx_lm import generate, load
    except ImportError as exc:
        raise QualitativeEvaluationError(
            "mlx-lm ausente. Instale com: python -m pip install -e '.[train]'"
        ) from exc

    model, tokenizer = load(model_name, adapter_path=adapter_path)
    try:
        responses = []
        for index, item in enumerate(prompts, start=1):
            messages = []
            if item.system:
                messages.append({"role": "system", "content": item.system})
            messages.append({"role": "user", "content": item.user})
            prompt = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            print(f"  prompt {index}/{len(prompts)}")
            response = generate(
                model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False
            )
            responses.append(response.strip())
        return responses
    finally:
        del model
        del tokenizer
        mx.clear_cache()
        gc.collect()


def blind_responses(
    prompts: list[EvaluationPrompt],
    base_responses: list[str],
    adapter_responses: list[str],
    *,
    seed: int,
) -> list[dict[str, object]]:
    if not (len(prompts) == len(base_responses) == len(adapter_responses)):
        raise ValueError("Prompts e respostas devem ter o mesmo tamanho.")
    rng = random.Random(seed)
    assignments: list[dict[str, object]] = []
    for index, (prompt, base, adapter) in enumerate(
        zip(prompts, base_responses, adapter_responses, strict=True), start=1
    ):
        adapter_is_a = bool(rng.getrandbits(1))
        assignments.append(
            {
                "id": index,
                "prompt": prompt.user,
                "response_a": adapter if adapter_is_a else base,
                "response_b": base if adapter_is_a else adapter,
                "model_a": "adapter" if adapter_is_a else "base",
                "model_b": "base" if adapter_is_a else "adapter",
            }
        )
    return assignments


def render_review(assignments: list[dict[str, object]]) -> str:
    lines = [
        "# Avaliação qualitativa cega",
        "",
        "Compare A e B sem abrir `answer_key.json`. Dê notas de 1 (ruim) a 5 (excelente).",
        "Em alucinação, use 1 para muita invenção e 5 para nenhuma invenção.",
        "",
    ]
    for item in assignments:
        lines.extend(
            [
                f"## Prompt {item['id']}",
                "",
                str(item["prompt"]),
                "",
                "### Resposta A",
                "",
                str(item["response_a"]),
                "",
                "### Resposta B",
                "",
                str(item["response_b"]),
                "",
                "| Critério | A (1–5) | B (1–5) |",
                "| --- | ---: | ---: |",
                "| Correção técnica |  |  |",
                "| Clareza |  |  |",
                "| Objetividade |  |  |",
                "| Português |  |  |",
                "| Aderência à instrução |  |  |",
                "| Ausência de alucinação |  |  |",
                "",
                "**Vencedor (A/B/empate):** ",
                "",
                "**Observações:** ",
                "",
            ]
        )
    return "\n".join(lines)


def render_answer_key(assignments: list[dict[str, object]], seed: int) -> dict[str, object]:
    return {
        "warning": "Abra somente depois de concluir review.md.",
        "seed": seed,
        "assignments": [
            {"prompt_id": item["id"], "A": item["model_a"], "B": item["model_b"]}
            for item in assignments
        ],
    }
