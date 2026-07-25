from __future__ import annotations

import importlib.util
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from llm_lab.config import ExperimentConfig, load_config
from llm_lab.project import find_project_root
from llm_lab.runner import validate_experiment


class TrainingPreflightError(RuntimeError):
    """Indica que o ambiente ainda não está pronto para treinamento."""


@dataclass(frozen=True)
class TrainingPlan:
    command: list[str]
    project_root: Path
    adapter_path: Path


def build_training_plan(config_path: str | Path) -> TrainingPlan:
    validated = validate_experiment(config_path)
    config = validated.config
    root = find_project_root(config.source)
    _require_approved_dataset(config, root)
    training = config.raw["training"]
    adapter_path = (root / config.raw["model"]["adapter_output"] / "exp_0001").resolve()
    command = [
        sys.executable, "-m", "mlx_lm.lora",
        "--model", config.model_base,
        "--train",
        "--data", str(config.train_file.parent),
        "--adapter-path", str(adapter_path),
        "--iters", str(training["iterations"]),
        "--batch-size", str(training["batch_size"]),
        "--num-layers", str(training["num_layers"]),
        "--learning-rate", str(training["learning_rate"]),
        "--max-seq-length", str(training["max_seq_length"]),
        "--save-every", str(training["save_every"]),
    ]
    if training.get("mask_prompt"):
        command.append("--mask-prompt")
    for key, flag in (("steps_per_report", "--steps-per-report"), ("steps_per_eval", "--steps-per-eval")):
        if key in training:
            command.extend([flag, str(training[key])])
    return TrainingPlan(command=command, project_root=root, adapter_path=adapter_path)


def preflight(plan: TrainingPlan, *, require_backend: bool) -> None:
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise TrainingPreflightError("O backend MLX exige macOS em Apple Silicon (arm64).")
    if require_backend and importlib.util.find_spec("mlx_lm") is None:
        raise TrainingPreflightError(
            "mlx-lm ausente. Instale com: python -m pip install -e '.[train]'"
        )
    if plan.adapter_path.exists() and any(plan.adapter_path.iterdir()):
        raise TrainingPreflightError(f"Diretório de adaptador não está vazio: {plan.adapter_path}")


def execute_training(config_path: str | Path) -> int:
    plan = build_training_plan(config_path)
    preflight(plan, require_backend=True)
    plan.adapter_path.mkdir(parents=True, exist_ok=False)
    return subprocess.run(plan.command, cwd=plan.project_root, check=False).returncode


def _require_approved_dataset(config: ExperimentConfig, root: Path) -> None:
    import yaml

    version = config.raw["dataset"]["version"]
    manifest = root / "datasets" / "versions" / version / "dataset.yaml"
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    if data.get("status") != "approved":
        raise TrainingPreflightError(f"Dataset {version} ainda não foi aprovado.")
