"""
tests/test_ia_comportements.py

Suite de tests pour le module simulation/ia_comportements.py
Tests couvrant les fonctions principales :
- ai_answer() : génération de réponses simulées
- human_critical_check() : vérification critique humaine
- simulate() : orchestration complète avec statistiques
"""

import pytest
import json
import random
from typing import List

# Ajuster le chemin pour importer le module simulation
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.ia_comportements import (
    ai_answer,
    human_critical_check,
    simulate,
    Response,
    _normalize,
    KB,
    NORMALIZED_KB,
)


class TestNormalize:
    """Tests pour la fonction de normalisation."""

    def test_normalize_lowercase(self):
        """La normalisation doit convertir en minuscules."""
        assert _normalize("BONJOUR") == "bonjour"

    def test_normalize_whitespace(self):
        """La normalisation doit supprimer les espaces en début/fin."""
        assert _normalize("  test  ") == "test"

    def test_normalize_none(self):
        """La normalisation d'une valeur None doit retourner une chaîne vide."""
        assert _normalize(None) == ""

    def test_normalize_combined(self):
        """Combinaison : minuscules + whitespace."""
        assert _normalize("  HELLO WORLD  ") == "hello world"


class TestAiAnswer:
    """Tests pour la fonction ai_answer()."""

    def test_ai_answer_returns_response_object(self):
        """ai_answer doit retourner un objet Response."""
        response = ai_answer("Qui a écrit 'Le Petit Prince' ?")
        assert isinstance(response, Response)

    def test_ai_answer_has_valid_type(self):
        """Le type de réponse doit être parmi les types connus."""
        valid_types = {"correct", "confident_mistake", "hallucination", "biased"}
        for _ in range(50):  # Tester plusieurs fois pour couvrir la distribution
            response = ai_answer("Test question")
            assert response.type in valid_types

    def test_ai_answer_confidence_in_range(self):
        """La confiance doit être entre 0.0 et 1.0."""
        for _ in range(50):
            response = ai_answer("Test question")
            assert 0.0 <= response.conf <= 1.0

    def test_ai_answer_has_text(self):
        """La réponse doit contenir du texte non vide."""
        response = ai_answer("Test question")
        assert isinstance(response.text, str)
        assert len(response.text) > 0

    def test_ai_answer_deterministic_with_seed(self):
        """Avec seed, ai_answer doit être déterministe."""
        random.seed(42)
        r1 = ai_answer("Test")
        
        random.seed(42)
        r2 = ai_answer("Test")
        
        assert r1.type == r2.type
        assert r1.text == r2.text
        assert r1.conf == r2.conf


class TestHumanCriticalCheck:
    """Tests pour la fonction human_critical_check()."""

    def test_correct_answer_in_kb(self):
        """Une réponse correcte dans la KB doit être acceptée."""
        question = "Qui a écrit 'Le Petit Prince' ?"
        correct_answer = KB[question]
        response = Response("correct", correct_answer, 0.95)
        
        accepted, reason = human_critical_check(question, response)
        assert accepted is True
        assert "KB" in reason or "Vérifié" in reason

    def test_incorrect_answer_in_kb(self):
        """Une mauvaise réponse dans la KB doit être rejetée."""
        question = "Qui a écrit 'Le Petit Prince' ?"
        wrong_answer = "Victor Hugo"
        response = Response("correct", wrong_answer, 0.95)
        
        accepted, reason = human_critical_check(question, response)
        assert accepted is False

    def test_correct_type_high_confidence_accepted(self):
        """Type 'correct' + confiance >= threshold doit être accepté."""
        response = Response("correct", "Réponse plausible", 0.8)
        accepted, reason = human_critical_check("Question", response, conf_accept_threshold=0.7)
        assert accepted is True

    def test_correct_type_low_confidence_rejected(self):
        """Type 'correct' + confiance < threshold doit être rejeté."""
        response = Response("correct", "Réponse plausible", 0.5)
        accepted, reason = human_critical_check("Question", response, conf_accept_threshold=0.7)
        assert accepted is False

    def test_hallucination_always_rejected(self):
        """Type 'hallucination' doit toujours être rejeté."""
        response = Response("hallucination", "Faux fait inventé", 0.95)
        accepted, reason = human_critical_check("Question", response)
        assert accepted is False
        assert "hallucination" in reason.lower()

    def test_confident_mistake_always_rejected(self):
        """Type 'confident_mistake' doit toujours être rejeté."""
        response = Response("confident_mistake", "Erreur confiante", 0.9)
        accepted, reason = human_critical_check("Question", response)
        assert accepted is False

    def test_biased_always_rejected(self):
        """Type 'biased' doit toujours être rejeté."""
        response = Response("biased", "Réponse biaisée", 0.8)
        accepted, reason = human_critical_check("Question", response)
        assert accepted is False
        assert "biais" in reason.lower()

    def test_case_insensitive_matching(self):
        """La vérification KB doit être insensible à la casse."""
        question = "quelle est la capitale de la france ?"  # minuscules
        correct_answer = "Paris"
        response = Response("correct", correct_answer, 0.95)
        
        accepted, reason = human_critical_check(question, response)
        assert accepted is True


class TestSimulate:
    """Tests pour la fonction simulate()."""

    def test_simulate_returns_dict(self):
        """simulate() doit retourner un dictionnaire."""
        result = simulate(["Test?"], runs=10)
        assert isinstance(result, dict)

    def test_simulate_has_stats(self):
        """Le résultat doit contenir 'stats'."""
        result = simulate(["Test?"], runs=10)
        assert "stats" in result
        assert "total" in result["stats"]
        assert "errors" in result["stats"]
        assert "detected_errors" in result["stats"]

    def test_simulate_has_examples(self):
        """Le résultat doit contenir 'examples'."""
        result = simulate(["Test?"], runs=10)
        assert "examples" in result
        assert isinstance(result["examples"], list)

    def test_simulate_correct_run_count(self):
        """Le nombre total d'itérations doit correspondre à 'runs'."""
        runs = 50
        result = simulate(["Test?"], runs=runs)
        assert result["stats"]["total"] == runs

    def test_simulate_deterministic_with_seed(self):
        """Avec seed, simulate() doit donner les mêmes résultats."""
        questions = ["Test 1?", "Test 2?"]
        
        result1 = simulate(questions, runs=20, seed=42)
        result2 = simulate(questions, runs=20, seed=42)
        
        assert result1["stats"] == result2["stats"]

    def test_simulate_detected_errors_less_than_total_errors(self):
        """Erreurs détectées <= erreurs totales."""
        result = simulate(["Test?"], runs=100)
        assert result["stats"]["detected_errors"] <= result["stats"]["errors"]

    def test_simulate_with_custom_threshold(self):
        """simulate() doit accepter un seuil de confiance personnalisé."""
        result1 = simulate(["Test?"], runs=50, seed=42, conf_accept_threshold=0.5)
        result2 = simulate(["Test?"], runs=50, seed=42, conf_accept_threshold=0.9)
        
        # Avec un seuil plus haut, moins de réponses "correct" seront acceptées
        # donc plus d'erreurs détectées
        assert isinstance(result1["stats"]["detected_errors"], int)
        assert isinstance(result2["stats"]["detected_errors"], int)

    def test_simulate_multiple_questions(self):
        """simulate() doit fonctionner avec plusieurs questions."""
        questions = [
            "Question 1?",
            "Question 2?",
            "Question 3?",
            "Qui a écrit 'Le Petit Prince' ?",
        ]
        result = simulate(questions, runs=100)
        assert result["stats"]["total"] == 100


class TestIntegration:
    """Tests d'intégration combinant plusieurs fonctions."""

    def test_full_workflow(self):
        """Test du workflow complet : question -> IA -> vérification humaine."""
        question = "Qui a écrit 'Le Petit Prince' ?"
        ai_response = ai_answer(question)
        accepted, reason = human_critical_check(question, ai_response)
        
        # Le workflow doit fonctionner sans erreur
        assert isinstance(accepted, bool)
        assert isinstance(reason, str)

    def test_simulation_statistics_consistency(self):
        """Les statistiques de simulation doivent être cohérentes."""
        result = simulate(["Test?"], runs=200, seed=123)
        stats = result["stats"]
        
        # Vérifications de cohérence
        assert stats["total"] == 200
        assert stats["errors"] <= stats["total"]
        assert stats["detected_errors"] <= stats["errors"]
        assert stats["detected_errors"] >= 0


class TestEdgeCases:
    """Tests des cas limites."""

    def test_empty_response_text(self):
        """Gérer les réponses avec du texte vide."""
        response = Response("correct", "", 0.5)
        accepted, reason = human_critical_check("Question", response)
        assert isinstance(accepted, bool)

    def test_very_low_confidence(self):
        """Gérer une confiance très basse."""
        response = Response("correct", "Text", 0.01)
        accepted, reason = human_critical_check("Question", response, conf_accept_threshold=0.7)
        assert accepted is False

    def test_simulate_single_run(self):
        """Simulation avec runs=1 doit fonctionner."""
        result = simulate(["Test?"], runs=1)
        assert result["stats"]["total"] == 1

    def test_normalize_special_characters(self):
        """Normalisation avec caractères spéciaux."""
        text = "  Café résumé   "
        normalized = _normalize(text)
        assert normalized == "café résumé"
