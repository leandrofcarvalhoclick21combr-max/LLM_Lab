from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class DatasetValidationError(ValueError):
    """Indica que um dataset não atende ao contrato conversacional."""


@dataclass(frozen=True)
class DatasetSummary:
    path: Path
    records: int


def validate_jsonl(path: str | Path) -> DatasetSummary:
    source = Path(path)
    if not source.is_file():
        raise DatasetValidationError(f"Dataset não encontrado: {source}")

    records = 0
    with source.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise DatasetValidationError(
                    f"JSON inválido em {source}:{line_number}: {exc.msg}"
                ) from exc
            _validate_record(row, source, line_number)
            records += 1

    if records == 0:
        raise DatasetValidationError(f"Dataset vazio: {source}")
    return DatasetSummary(path=source, records=records)


def _validate_record(row: Any, source: Path, line_number: int) -> None:
    if not isinstance(row, dict) or not isinstance(row.get("messages"), list):
        raise DatasetValidationError(
            f"Registro em {source}:{line_number} deve conter a lista 'messages'."
        )
    messages = row["messages"]
    if not messages:
        raise DatasetValidationError(f"Lista 'messages' vazia em {source}:{line_number}.")

    roles: list[str] = []
    for message in messages:
        if not isinstance(message, dict):
            raise DatasetValidationError(f"Mensagem inválida em {source}:{line_number}.")
        role = message.get("role")
        content = message.get("content")
        if role not in {"system", "user", "assistant"}:
            raise DatasetValidationError(f"Role inválido em {source}:{line_number}: {role!r}")
        if not isinstance(content, str) or not content.strip():
            raise DatasetValidationError(f"Conteúdo vazio em {source}:{line_number}.")
        roles.append(role)

    if "user" not in roles or "assistant" not in roles:
        raise DatasetValidationError(
            f"Registro em {source}:{line_number} precisa de mensagens user e assistant."
        )
