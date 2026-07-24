from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from llm_lab.config import ExperimentConfig
from llm_lab.datasets import DatasetSummary


@dataclass(frozen=True)
class ExperimentRecord:
    experiment_id: str
    directory: Path


def create_experiment(
    config: ExperimentConfig,
    datasets: list[DatasetSummary],
    project_root: Path,
) -> ExperimentRecord:
    import yaml

    index_path = project_root / "experiments" / "index.yaml"
    index = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    entries = index.get("experiments")
    if not isinstance(entries, list):
        raise ValueError("experiments/index.yaml possui campo 'experiments' inválido.")

    experiment_id = _next_id(entries)
    directory = project_root / "experiments" / experiment_id
    if directory.exists():
        raise FileExistsError(f"Experimento já existe: {directory}")

    for child in ("logs", "artifacts", "results"):
        (directory / child).mkdir(parents=True, exist_ok=False)

    created_at = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "id": experiment_id,
        "name": config.name,
        "status": "created",
        "created_at": created_at,
        "model": config.model_base,
        "config_source": str(config.source.relative_to(project_root)),
        "datasets": [
            {"path": str(item.path.relative_to(project_root)), "records": item.records}
            for item in datasets
        ],
        "configuration": config.raw,
    }
    (directory / "experiment.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (directory / "report.md").write_text(
        f"# {experiment_id} — {config.name}\n\n"
        "**Status:** criado\n\n"
        "A configuração e os datasets foram validados. O backend de treinamento "
        "ainda não foi executado.\n",
        encoding="utf-8",
    )

    entries.append(
        {"id": experiment_id, "name": config.name, "status": "created", "created_at": created_at}
    )
    index["latest"] = experiment_id
    index.setdefault("best_experiment", None)
    index_path.write_text(
        yaml.safe_dump(index, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    return ExperimentRecord(experiment_id=experiment_id, directory=directory)


def _next_id(entries: list[dict[str, Any]]) -> str:
    numbers = []
    for entry in entries:
        value = entry.get("id") if isinstance(entry, dict) else None
        if isinstance(value, str) and value.startswith("exp_") and value[4:].isdigit():
            numbers.append(int(value[4:]))
    return f"exp_{max(numbers, default=0) + 1:04d}"
