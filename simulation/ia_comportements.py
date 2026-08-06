# "simulation_ia_comportements.py
# Simule comportements d'une IA et la vérification critique humaine.

import random
from typing import Dict, Tuple

# Petite base de connaissances factuelle pour vérification
KB = {
    "Qui a écrit 'Le Petit Prince' ?": "Antoine de Saint-Exupéry",
    "Quelle est la capitale de la France ?": "Paris",
    "2+2 = ?": "4",
}


def ai_answer(question: str) -> Dict:
    """
    Retourne un dict avec 'text' et 'type' : 'correct', 'confident_mistake', 'hallucination', 'biased'
    Les probabilités sont artificielles pour la simulation.
    """
    r = random.random()
    if r < 0.6:
        # bonne réponse basée sur KB si possible, sinon réponse générique correcte
        text = KB.get(question, "Voici une réponse plausible mais simplifiée.")
        return {"type": "correct", "text": text, "conf": round(random.uniform(0.7, 1.0), 2)}
    if r < 0.8:
        # erreur confiante : réponse plausible mais incorrecte
        text = "Ceci est une réponse plausible mais incorrecte."
        return {"type": "confident_mistake", "text": text, "conf": round(random.uniform(0.85, 1.0), 2)}
    if r < 0.95:
        # hallucination : invente un fait (ex: attribue faussement une citation)
        text = "Selon le rapport X (non référencé), cela marche ainsi."
        return {"type": "hallucination", "text": text, "conf": round(random.uniform(0.6, 0.95), 2)}
    # biais : réponse stéréotypée ou orientée
    text = "D'après mon entraînement, le groupe Y a tendance à ... (biais possible)."
    return {"type": "biased", "text": text, "conf": round(random.uniform(0.5, 0.9), 2)}


def human_critical_check(question: str, ai_resp: Dict) -> Tuple[bool, str]:
    """
    Simule une vérification critique de l'humain :
    - demande de source si l'IA est très confiante ou si on soupçonne hallucination
    - vérifie dans la base KB si possible
    - pose une question de contrôle (contre-factuelle) pour détecter l'incohérence
    Retourne (accepté_bool, raison)
    """
    # Si la question est dans la KB, vérification facile
    if question in KB:
        correct = KB[question]
        if ai_resp["text"] == correct:
            return True, "Vérifié dans KB — correct."
        else:
            return False, f"Contradiction avec KB (attendu: {correct})."
    # Pour réponses hors KB, on applique des heuristiques
    if ai_resp["type"] == "hallucination":
        return False, "Pas de source, ressemble à une hallucination."
    if ai_resp["type"] == "confident_mistake":
        # possible acceptation partielle mais on recommande la vérification
        return False, "Erreur probable malgré la confiance — demander sources."
    if ai_resp["type"] == "biased":
        return False, "Réponse potentiellement biaisée — demander reformulation et sources."
    # fallback
    return False, "Incertain — demander sources et preuves."


def simulate(questions: list, runs: int = 200):
    stats = {"total": 0, "detected_errors": 0, "errors": 0}
    examples = []
    for _ in range(runs):
        q = random.choice(questions)
        ai = ai_answer(q)
        accepted, reason = human_critical_check(q, ai)
        stats["total"] += 1
        if ai["type"] != "correct":
            stats["errors"] += 1
        if not accepted and ai["type"] != "correct":
            stats["detected_errors"] += 1
        # Collect quelques exemples
        if len(examples) < 6 and ai["type"] != "correct":
            examples.append({"q": q, "ai": ai, "check": reason})
    # Résultats
    print("Simulation — résultats")
    print(f"Total itérations : {stats['total']}")
    print(f"Erreurs IA (simulées) : {stats['errors']}")
    print(f"Erreurs détectées par l'humain critique : {stats['detected_errors']}")
    print("\nExemples d'erreurs détectées :")
    for e in examples:
        print("Q:", e["q"])
        print("IA:", e["ai"]["text"], f"(type={e['ai']['type']}, conf={e['ai']['conf']})")
        print("Vérification:", e["check"])
        print("-" * 30)


if __name__ == '__main__':
    QUESTIONS = [
        "Qui a écrit 'Le Petit Prince' ?",
        "Quelle est la capitale de la France ?",
        "2+2 = ?",
        "Explique pourquoi X cause Y.",
        "Donne une méthode pour résoudre un problème éthique.",
    ]
    simulate(QUESTIONS, runs=300)"
