from llm_lab.experiments import _next_id


def test_next_id_ignores_invalid_entries():
    assert _next_id([{"id": "exp_0002"}, {"id": "manual"}, {}]) == "exp_0003"
