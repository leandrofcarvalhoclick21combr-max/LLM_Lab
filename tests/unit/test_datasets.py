import json

import pytest

from llm_lab.datasets import DatasetValidationError, validate_jsonl


def test_validate_jsonl_accepts_conversation(tmp_path):
    path = tmp_path / "data.jsonl"
    path.write_text(
        json.dumps(
            {
                "messages": [
                    {"role": "user", "content": "Oi"},
                    {"role": "assistant", "content": "Olá"},
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )

    summary = validate_jsonl(path)

    assert summary.records == 1


def test_validate_jsonl_rejects_missing_assistant(tmp_path):
    path = tmp_path / "data.jsonl"
    path.write_text('{"messages":[{"role":"user","content":"Oi"}]}\n', encoding="utf-8")

    with pytest.raises(DatasetValidationError, match="user e assistant"):
        validate_jsonl(path)
