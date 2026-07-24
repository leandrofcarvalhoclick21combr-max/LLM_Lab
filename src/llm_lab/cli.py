from __future__ import annotations

import argparse
import sys

from llm_lab.config import ConfigurationError
from llm_lab.datasets import DatasetValidationError
from llm_lab.experiments import ExperimentRecord
from llm_lab.runner import ValidationResult, run_experiment, validate_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Valida configuração e datasets.")
    validate.add_argument("config")

    run = subparsers.add_parser("run", help="Registra um novo experimento validado.")
    run.add_argument("config")
    run.add_argument("--dry-run", action="store_true", help="Valida sem criar arquivos.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_experiment(args.config)
        else:
            result = run_experiment(args.config, dry_run=args.dry_run)
    except (ConfigurationError, DatasetValidationError, ValueError, OSError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2

    _print_result(result)
    return 0


def _print_result(result: ValidationResult | ExperimentRecord) -> None:
    if isinstance(result, ExperimentRecord):
        print(f"Experimento criado: {result.experiment_id}")
        print(f"Diretório: {result.directory}")
        return
    print(f"Configuração válida: {result.config.source}")
    for dataset in result.datasets:
        print(f"Dataset válido: {dataset.path} ({dataset.records} registros)")
