from llm_lab.project import find_project_root


def test_find_project_root_from_nested_config(tmp_path):
    nested = tmp_path / "configs" / "training"
    nested.mkdir(parents=True)
    (tmp_path / "experiments").mkdir()
    (tmp_path / "experiments" / "index.yaml").write_text("experiments: []\n")
    config = nested / "model.yaml"
    config.write_text("model: {}\n")

    assert find_project_root(config) == tmp_path
