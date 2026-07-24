import importlib.util
from pathlib import Path


def _module():
    path = Path(__file__).parents[2] / "scripts" / "build_dataset_v1.py"
    spec = importlib.util.spec_from_file_location("build_dataset_v1", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_catalog_has_expected_sizes_and_isolated_concepts():
    module = _module()
    assert len(module.TRAIN) == 52
    assert len(module.VALID) == 10
    assert len(module.TEST) == 5

    splits = [{term.casefold() for term, _ in items} for items in (module.TRAIN, module.VALID, module.TEST)]
    assert splits[0].isdisjoint(splits[1])
    assert splits[0].isdisjoint(splits[2])
    assert splits[1].isdisjoint(splits[2])


def test_generated_examples_are_unique_and_complete():
    module = _module()
    rows = module.examples(module.TRAIN) + module.examples(module.VALID) + module.examples(module.TEST)
    prompts = [row["messages"][1]["content"] for row in rows]
    answers = [row["messages"][2]["content"] for row in rows]
    assert len(rows) == 134
    assert len(prompts) == len(set(prompts))
    assert len(answers) == len(set(answers))
