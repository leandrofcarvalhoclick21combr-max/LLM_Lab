from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from llm_lab.config import ExperimentConfig, load_config
from llm_lab.datasets import DatasetSummary, validate_jsonl
from llm_lab.experiments import ExperimentRecord, create_experiment
from llm_lab.project import find_project_root


@dataclass(frozen=True)
class ValidationResult:
    config: ExperimentConfig
    datasets: list[DatasetSummary]


def validate_experiment(config_path: str | Path) -> ValidationResult:
    config = load_config(config_path)
    datasets = [
        validate_jsonl(config.train_file),
        validate_jsonl(config.valid_file),
        validate_jsonl(config.test_file),
    ]
    return ValidationResult(config=config, datasets=datasets)


def run_experiment(
    config_path: str | Path, *, dry_run: bool = False
) -> ValidationResult | ExperimentRecord:
    validated = validate_experiment(config_path)
    if dry_run:
        return validated
    project_root = find_project_root(validated.config.source)
    return create_experiment(validated.config, validated.datasets, project_root)
