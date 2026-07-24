import json

import yaml

from llm_lab.experiments import ExperimentRecord
from llm_lab.runner import run_experiment


def test_runner_creates_registered_experiment(tmp_path):
    (tmp_path / "configs").mkdir()
    (tmp_path / "datasets" / "versions" / "v1").mkdir(parents=True)
    (tmp_path / "experiments").mkdir()
    (tmp_path / "experiments" / "index.yaml").write_text(
        "latest: null\nbest_experiment: null\nexperiments: []\n", encoding="utf-8"
    )
    row = json.dumps(
        {
            "messages": [
                {"role": "user", "content": "Oi"},
                {"role": "assistant", "content": "Olá"},
            ]
        }
    )
    for split in ("train", "valid", "test"):
        (tmp_path / "datasets" / "versions" / "v1" / f"{split}.jsonl").write_text(
            row + "\n", encoding="utf-8"
        )
    config = {
        "experiment": {"name": "integration"},
        "model": {"base": "example/model"},
        "dataset": {
            "train_file": "datasets/versions/v1/train.jsonl",
            "valid_file": "datasets/versions/v1/valid.jsonl",
            "test_file": "datasets/versions/v1/test.jsonl",
        },
        "training": {
            "iterations": 1,
            "batch_size": 1,
            "learning_rate": 0.001,
            "max_seq_length": 64,
            "save_every": 1,
        },
    }
    config_path = tmp_path / "configs" / "test.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

    result = run_experiment(config_path)

    assert isinstance(result, ExperimentRecord)
    assert result.experiment_id == "exp_0001"
    assert (result.directory / "experiment.yaml").is_file()
    index = yaml.safe_load(
        (tmp_path / "experiments" / "index.yaml").read_text(encoding="utf-8")
    )
    assert index["latest"] == "exp_0001"
