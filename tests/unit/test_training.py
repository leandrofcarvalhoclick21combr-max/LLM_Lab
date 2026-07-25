from pathlib import Path

import pytest

from llm_lab.training import TrainingPlan, TrainingPreflightError, preflight


def test_preflight_rejects_non_apple_silicon(monkeypatch, tmp_path):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr("platform.machine", lambda: "x86_64")
    plan = TrainingPlan(["python", "-m", "mlx_lm.lora"], tmp_path, tmp_path / "adapter")
    with pytest.raises(TrainingPreflightError, match="Apple Silicon"):
        preflight(plan, require_backend=False)


def test_preflight_rejects_existing_adapter(monkeypatch, tmp_path):
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr("platform.machine", lambda: "arm64")
    adapter = tmp_path / "adapter"
    adapter.mkdir()
    (adapter / "weights.safetensors").write_text("existing")
    plan = TrainingPlan(["python", "-m", "mlx_lm.lora"], tmp_path, adapter)
    with pytest.raises(TrainingPreflightError, match="não está vazio"):
        preflight(plan, require_backend=False)
