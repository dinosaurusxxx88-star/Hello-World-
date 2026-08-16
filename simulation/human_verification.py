# simulation/human_verification.py
# Module de vérification critique humaine - INDÉPENDANT de la génération IA
# 
# Vision: L'humain reçoit UNIQUEMENT le texte, la confiance et la question.
# L'humain NE VOIT PAS le "type" généré par l'IA.
# Cela simule une vérification critique humaine réelle.

import json
from typing import Tuple, Optional, Dict
from pathlib import Path


def load_knowledge_base(kb_path: str) -> Dict[str, str]:
    """
    Charge la base de connaissances depuis un fichier JSON.
    
    Args:
        kb_path: Chemin vers knowledge_base.json
        
    Returns:
        Dict avec question -> réponse
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si le JSON est invalide
    """
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        if not isinstance(kb, dict):
            raise ValueError("knowledge_base.json doit être un dictionnaire")
        return kb
    except FileNotFoundError:
        raise FileNotFoundError(f"knowledge_base.json non trouvé: {kb_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"knowledge_base.json invalide: {e}")


def normalize_text(text: Optional[str]) -> str:
    """Normalise une chaîne pour comparaison."""
    if text is None or text == "":
        return ""
    return text.lower().strip()


def build_normalized_kb(kb: Dict[str, str]) -> Dict[str, str]:
    """Construit une KB normalisée (clé normalisée -> valeur originale)."""
    return {normalize_text(k): v for k, v in kb.items()}


def verify_against_kb(
    question: str,
    ai_text: str,
    kb: Dict[str, str]
) -> Tuple[Optional[bool], str]:
    """
    Vérifie si la réponse IA correspond à la KB.
    
    Returns:
        (acceptée: bool, raison: str)
        acceptée est None si question non trouvée dans KB
    """
    normalized_kb = build_normalized_kb(kb)
    q_norm = normalize_text(question)
    ai_text_norm = normalize_text(ai_text)
    
    if q_norm in normalized_kb:
        expected = normalize_text(normalized_kb[q_norm])
        if ai_text_norm == expected:
            return True, "Vérifié dans KB — réponse correcte."
        else:
            return False, f"Contradiction avec KB (attendu: {normalized_kb[q_norm]})."
    
    # Question non dans KB
    return None, "Question non dans KB — vérification impossible."


def human_critical_check(
    ai_text: str,
    ai_confidence: float,
    question: str,
    kb: Dict[str, str],
    confidence_threshold: float = 0.7
) -> Tuple[bool, str]:
    """
    Simule une vérification critique HUMAINE.
    
    L'humain reçoit UNIQUEMENT:
    - ai_text: Texte de la réponse
    - ai_confidence: Confiance annoncée
    - question: La question
    - kb: La base de connaissances pour vérification
    
    L'humain NE VOIT PAS le "type" généré par l'IA.
    Cela simule une vérification réelle, indépendante de la génération.
    
    Stratégie de vérification humaine :
    1. Vérifier via KB si possible (fait objectif)
    2. Détecter signes de hallucination (absence de source)
    3. Détecter biais (formulations stéréotypées)
    4. Accepter/rejeter selon confiance et anomalies détectées
    
    Returns:
        (acceptée: bool, raison: str)
    """
    # ÉTAPE 1: Vérification directe via KB
    kb_result, kb_reason = verify_against_kb(question, ai_text, kb)
    
    if kb_result is True:
        return True, kb_reason
    elif kb_result is False:
        return False, kb_reason
    
    # ÉTAPE 2: Question non dans KB → heuristiques
    text_lower = ai_text.lower()
    
    # Détection hallucination: affirmation sans source
    if ("rapport" in text_lower or "source" in text_lower) and \
       ("non référencé" in text_lower or "non cité" in text_lower):
        return False, "Pas de source verifiable — hallucination probable."
    
    # Détection hallucination: références vagues
    if "selon" in text_lower and ")" not in ai_text:
        return False, "Affirmation sans source précise — demander justification."
    
    # Détection biais: formulation stéréotypée
    if ("groupe" in text_lower or "minorité" in text_lower) and \
       ("tendance" in text_lower or "stereotype" in text_lower.replace("é", "e")):
        return False, "Formulation potentiellement biaisée — demander reformulation."
    
    # ÉTAPE 3: Pas d'anomalie détectée → décision selon confiance
    if ai_confidence >= confidence_threshold:
        return True, f"Accepté (confiance {ai_confidence:.2f} >= {confidence_threshold}, contenu plausible)."
    else:
        return False, f"Confiance insuffisante ({ai_confidence:.2f} < {confidence_threshold})."
