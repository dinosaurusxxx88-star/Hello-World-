import random

from simulation import ia_comportements as ia


def test_ai_answer_type_and_confidence():
    # deterministic seed for reproducibility
    random.seed(0)
    resp = ia.ai_answer("Quel âge a le Petit Prince ?")
    assert resp.type in {"correct", "confident_mistake", "hallucination", "biased"}
    assert isinstance(resp.conf, float)
    assert 0.0 <= resp.conf <= 1.0


def test_human_critical_check_accepts_high_conf_correct():
    resp = ia.Response(type="correct", text="Paris", conf=0.95)
    accepted, reason = ia.human_critical_check(
        "Où est la capitale de la France ?", resp, conf_accept_threshold=0.9
    )
    assert accepted is True


def test_human_critical_check_rejects_confident_mistake():
    resp = ia.Response(type="confident_mistake", text="London", conf=0.9)
    accepted, reason = ia.human_critical_check(
        "Où est la capitale de la France ?", resp, conf_accept_threshold=0.8
    )
    assert accepted is False
