from __future__ import annotations
# simulation/ia_comportements.py
# Simule comportements d'une IA et la vérification critique humaine.

import argparse
import json
import random
from dataclasses import dataclass, asdict
from typing import Dict, Tuple, List, Any

# Petite base de connaissances factuelle pour vérification (clé originale -> valeur)
KB = {
    "Qui a écrit 'Le Petit Prince' ?": "Antoine de Saint-Exupéry",
    "Quelle est la capitale de la France ?": "Paris",
    "2+2 = ?": "4",
}

# Normaliser les questions/réponses pour comparaison simple
def _normalize(text: str) -> str:
    return "" if text is None else text.lower().strip()

# Construire une KB normalisée (question_normalisée -> réponse originale)
NORMALIZED_KB: Dict[str, str] = { _normalize(k): v for k, v in KB.items() }


@dataclass
class Response:
    type: str
    text: str
    conf: float


def ai_answer(question: str) -> Response:
    """
    Retourne une Response simulant le comportement d'une IA:
    types: 'correct', 'confident_mistake', 'hallucination', 'biased'
    Les probabilités sont artificielles pour la simulation.
    """
    r = random.random()
    if r < 0.6:
        # bonne réponse basée sur KB si possible, sinon réponse générique correcte
        text = KB.get(question, "Voici une réponse plausible mais simplifiée.")
        return Response("correct", text, round(random.uniform(0.7, 1.0), 2))
    if r < 0.8:
        # erreur confiante : réponse plausible mais incorrecte
        text = "Ceci est une réponse plausible mais incorrecte."
        return Response("confident_mistake", text, round(random.uniform(0.85, 1.0), 2))
    if r < 0.95:
        # hallucination : invente un fait (ex: attribue faussement une citation)
        text = "Selon le rapport X (non référencé), cela marche ainsi."
        return Response("hallucination", text, round(random.uniform(0.6, 0.95), 2))
    # biais : réponse stéréotypée ou orientée
    text = "D'après mon entraînement, le groupe Y a tendance à ... (biais possible)."
    return Response("biased", text, round(random.uniform(0.5, 0.9), 2))


def human_critical_check(question: str, ai_resp: Response, conf_accept_threshold: float = 0.7) -> Tuple[bool, str]:
    """
    Simule une vérification critique de l'humain :
    - normalise les chaînes
    - vérifie dans la base KB si possible (comparaison normalisée)
    - accepte les réponses marquées 'correct' si la confiance est >= conf_accept_threshold
    - retourne (accepted_bool, raison)
    """
    qn = _normalize(question)
    ai_text_norm = _normalize(ai_resp.text)

    # Vérification directe via KB (comparaison normalisée)
    if qn in NORMALIZED_KB:
        correct = NORMALIZED_KB[qn]
        if ai_text_norm == _normalize(correct):
            return True, "Vérifié dans KB — correct."
        else:
            return False, f"Contradiction avec KB (attendu: {correct})."

    # Acceptation si IA indique 'correct' et confiance suffisante
    if ai_resp.type == "correct" and ai_resp.conf >= conf_accept_threshold:
        return True, f"Accepté (type=correct, conf={ai_resp.conf} >= {conf_accept_threshold})."

    # Heuristiques pour autres types
    if ai_resp.type == "hallucination":
        return False, "Pas de source, ressemble à une hallucination."
    if ai_resp.type == "confident_mistake":
        return False, "Erreur probable malgré la confiance — demander sources."
    if ai_resp.type == "biased":
        return False, "Réponse potentiellement biaisée — demander reformulation et sources."

    # fallback
    return False, "Incertain — demander sources et preuves."


def simulate(questions: List[str], runs: int = 200, seed: int | None = None, conf_accept_threshold: float = 0.7) -> Dict[str, Any]:
    """
    Exécute la simulation et retourne des résultats structurés.
    """
    if seed is not None:
        random.seed(seed)

    stats = {"total": 0, "detected_errors": 0, "errors": 0}
    examples: List[Dict[str, Any]] = []

    for _ in range(runs):
        q = random.choice(questions)
        ai = ai_answer(q)
        accepted, reason = human_critical_check(q, ai, conf_accept_threshold)
        stats["total"] += 1
        if ai.type != "correct":
            stats["errors"] += 1
        if not accepted and ai.type != "correct":
            stats["detected_errors"] += 1
        # Collect quelques exemples (limités)
        if len(examples) < 6 and ai.type != "correct":
            examples.append({"q": q, "ai": asdict(ai), "check": reason})

    result = {
        "stats": stats,
        "examples": examples,
    }
    return result


def _print_results(res: Dict[str, Any]) -> None:
    stats = res["stats"]
    print("Simulation — résultats")
    print(f"Total itérations : {stats['total']}")
    print(f"Erreurs IA (simulées) : {stats['errors']}")
    print(f"Erreurs détectées par l'humain critique : {stats['detected_errors']}")
    print("\nExemples d'erreurs détectées :")
    for e in res["examples"]:
        print("Q:", e["q"])
        ai = e["ai"]
        print("IA:", ai["text"], f"(type={ai['type']}, conf={ai['conf']})")
        print("Vérification:", e["check"])
        print("-" * 30)


def _default_questions() -> List[str]:
    return [
        "Qui a écrit 'Le Petit Prince' ?",
        "Quelle est la capitale de la France ?",
        "2+2 = ?",
        "Explique pourquoi X cause Y.",
        "Donne une méthode pour résoudre un problème éthique.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulateur de comportements d'IA et vérification critique humaine")
    parser.add_argument("--runs", type=int, default=300, help="Nombre d'itérations de la simulation")
    parser.add_argument("--seed", type=int, default=None, help="Seed pour la reproductibilité (optionnel)")
    parser.add_argument("--questions-file", type=str, default=None, help="Fichier (JSON list) de questions à utiliser")
    parser.add_argument("--conf-accept-threshold", type=float, default=0.7, help="Seuil de confiance pour accepter une réponse marquée 'correct'")
    parser.add_argument("--json-output", action="store_true", help="Afficher la sortie en JSON au lieu d'un résumé lisible")

    args = parser.parse_args()

    if args.questions_file:
        try:
            with open(args.questions_file, 'r', encoding='utf-8') as f:
                questions = json.load(f)
                if not isinstance(questions, list):
                    raise ValueError("Le fichier de questions doit contenir une liste JSON.")
        except Exception as e:
            print(f"Erreur en lisant le fichier de questions: {e}")
            return
    else:
        questions = _default_questions()

    res = simulate(questions, runs=args.runs, seed=args.seed, conf_accept_threshold=args.conf_accept_threshold)

    if args.json_output:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        _print_results(res)


if __name__ == '__main__':
    main()
