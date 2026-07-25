from __future__ import annotations

import argparse
import shlex
import sys

from llm_lab.config import ConfigurationError
from llm_lab.datasets import DatasetValidationError
from llm_lab.evaluation import QualitativeEvaluationError, run_qualitative_evaluation
from llm_lab.experiments import ExperimentRecord
from llm_lab.runner import ValidationResult, run_experiment, validate_experiment
from llm_lab.training import TrainingPreflightError, build_training_plan, execute_training, preflight


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Valida configuração e datasets.")
    validate.add_argument("config")

    run = subparsers.add_parser("run", help="Registra um novo experimento validado.")
    run.add_argument("config")
    run.add_argument("--dry-run", action="store_true", help="Valida sem criar arquivos.")

    train = subparsers.add_parser("train", help="Planeja ou executa fine-tuning LoRA com MLX.")
    train.add_argument("config")
    train.add_argument("--execute", action="store_true", help="Executa o treinamento após o preflight.")

    qualitative = subparsers.add_parser(
        "evaluate-qualitative",
        help="Gera uma comparação cega entre modelo-base e adapter.",
    )
    qualitative.add_argument("experiment", help="ID do experimento, por exemplo exp_0001.")
    qualitative.add_argument(
        "--seed", type=int, default=42, help="Seed usada para embaralhar respostas A/B."
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_experiment(args.config)
        elif args.command == "run":
            result = run_experiment(args.config, dry_run=args.dry_run)
        elif args.command == "train":
            plan = build_training_plan(args.config)
            preflight(plan, require_backend=args.execute)
            print("Comando de treinamento:")
            print(shlex.join(plan.command))
            if not args.execute:
                print("Planejamento concluído; use --execute para iniciar.")
                return 0
            return execute_training(args.config)
        else:
            output = run_qualitative_evaluation(args.experiment, seed=args.seed)
            print(f"Avaliação gerada para {output.prompts} prompts.")
            print(f"Formulário: {output.review_path}")
            print(f"Gabarito: {output.answer_key_path}")
            return 0
    except (
        ConfigurationError,
        DatasetValidationError,
        QualitativeEvaluationError,
        TrainingPreflightError,
        ValueError,
        OSError,
    ) as exc:
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
