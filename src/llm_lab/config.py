from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from llm_lab.project import find_project_root


class ConfigurationError(ValueError):
    """Indica que uma configuração de experimento é inválida."""


@dataclass(frozen=True)
class ExperimentConfig:
    source: Path
    raw: dict[str, Any]
    name: str
    model_base: str
    train_file: Path
    valid_file: Path
    test_file: Path


def load_config(path: str | Path) -> ExperimentConfig:
    source = Path(path).resolve()
    if not source.is_file():
        raise ConfigurationError(f"Configuração não encontrada: {source}")

    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise ConfigurationError(
            "Dependência PyYAML ausente. Instale o projeto com: pip install -e ."
        ) from exc

    try:
        raw = yaml.safe_load(source.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"YAML inválido em {source}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigurationError("A raiz da configuração deve ser um objeto YAML.")

    name = _string(raw, "experiment", "name")
    model_base = _string(raw, "model", "base")
    train_file = _project_path(source, _string(raw, "dataset", "train_file"))
    valid_file = _project_path(source, _string(raw, "dataset", "valid_file"))
    test_file = _project_path(source, _string(raw, "dataset", "test_file"))

    training = _mapping(raw, "training")
    for field in ("iterations", "batch_size", "max_seq_length", "save_every"):
        value = training.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ConfigurationError(f"training.{field} deve ser um inteiro positivo.")

    learning_rate = training.get("learning_rate")
    if (
        not isinstance(learning_rate, (int, float))
        or isinstance(learning_rate, bool)
        or learning_rate <= 0
    ):
        raise ConfigurationError("training.learning_rate deve ser um número positivo.")

    return ExperimentConfig(
        source=source,
        raw=raw,
        name=name,
        model_base=model_base,
        train_file=train_file,
        valid_file=valid_file,
        test_file=test_file,
    )


def _mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ConfigurationError(f"Seção obrigatória ausente ou inválida: {key}")
    return value


def _string(data: dict[str, Any], section: str, field: str) -> str:
    value = _mapping(data, section).get(field)
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{section}.{field} deve ser um texto não vazio.")
    return value.strip()


def _project_path(config_path: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    project_root = find_project_root(config_path)
    return (project_root / candidate).resolve()
