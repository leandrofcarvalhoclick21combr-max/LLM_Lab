import json

from llm_lab.evaluation import (
    EvaluationPrompt,
    blind_responses,
    build_messages,
    clean_response,
    load_prompts,
    render_answer_key,
    render_review,
)


def test_load_prompts_ignores_reference_answers(tmp_path):
    source = tmp_path / "test.jsonl"
    source.write_text(
        json.dumps(
            {
                "messages": [
                    {"role": "system", "content": "Seja claro."},
                    {"role": "user", "content": "O que é LoRA?"},
                    {"role": "assistant", "content": "Resposta de referência."},
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )

    assert load_prompts(source) == [EvaluationPrompt("Seja claro.", "O que é LoRA?")]


def test_blind_responses_is_reproducible_and_preserves_pairs():
    prompts = [EvaluationPrompt("", "P1"), EvaluationPrompt("", "P2")]
    first = blind_responses(prompts, ["B1", "B2"], ["A1", "A2"], seed=7)
    second = blind_responses(prompts, ["B1", "B2"], ["A1", "A2"], seed=7)

    assert first == second
    for index, item in enumerate(first, start=1):
        assert {item["response_a"], item["response_b"]} == {f"B{index}", f"A{index}"}
        assert {item["model_a"], item["model_b"]} == {"base", "adapter"}


def test_review_hides_models_and_answer_key_reveals_them():
    assignments = blind_responses(
        [EvaluationPrompt("", "Explique RLHF")], ["Primeira resposta"], ["Segunda resposta"], seed=1
    )

    review = render_review(assignments)
    answer_key = render_answer_key(assignments, seed=1)

    assert "Resposta A" in review
    assert "Resposta B" in review
    assert "modelo-base" not in review
    assert "adapter" not in review.casefold()
    assert {answer_key["assignments"][0]["A"], answer_key["assignments"][0]["B"]} == {
        "base",
        "adapter",
    }


def test_messages_force_final_answer_in_portuguese_without_thinking():
    messages = build_messages(EvaluationPrompt("Seja preciso.", "Explique LoRA."))

    assert messages[0]["role"] == "system"
    assert "português do Brasil" in messages[0]["content"]
    assert "sem expor raciocínio interno" in messages[0]["content"]
    assert messages[1] == {"role": "user", "content": "Explique LoRA."}


def test_clean_response_removes_internal_thinking():
    response = "<think>Internal reasoning in English.</think>\n\nResposta final em português."

    assert clean_response(response) == "Resposta final em português."
