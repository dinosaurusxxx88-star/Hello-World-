# simulation/metrics.py
# Calcul des métriques de performance (matrice confusion, précision, recall, F1)

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ConfusionMatrix:
    """Matrice de confusion pour évaluation de la détection."""
    tp: int = 0  # Vrai Positif: IA erreur, humain rejette ✓
    fp: int = 0  # Faux Positif: IA correct, humain rejette ✗
    fn: int = 0  # Faux Négatif: IA erreur, humain accepte ✗
    tn: int = 0  # Vrai Négatif: IA correct, humain accepte ✓
    
    def __post_init__(self):
        """Valide que la somme est cohérente."""
        total = self.tp + self.fp + self.fn + self.tn
        if total == 0:
            raise ValueError("Matrice confusion vide (total = 0)")


@dataclass
class Metrics:
    """Métriques de performance."""
    precision: float
    recall: float
    f1: float
    specificity: float
    accuracy: float
    
    def __str__(self) -> str:
        return (
            f"Precision: {self.precision:.3f} | "
            f"Recall: {self.recall:.3f} | "
            f"F1-Score: {self.f1:.3f} | "
            f"Specificity: {self.specificity:.3f} | "
            f"Accuracy: {self.accuracy:.3f}"
        )


def compute_confusion_matrix(
    results: list[Dict[str, Any]]
) -> ConfusionMatrix:
    """
    Calcule la matrice de confusion à partir des résultats de simulation.
    
    Chaque résultat doit contenir:
    - is_correct (bool): Vérité terrain
    - human_accepted (bool): Décision humaine
    
    Args:
        results: Liste des résultats de simulation
        
    Returns:
        ConfusionMatrix avec TP, FP, FN, TN
    """
    cm = ConfusionMatrix()
    
    for result in results:
        is_correct = result.get("is_correct")
        human_accepted = result.get("human_accepted")
        
        if is_correct is None or human_accepted is None:
            continue
        
        # Vrai = erreur détectée, Faux = erreur non détectée
        is_error = not is_correct
        error_detected = not human_accepted
        
        if is_error and error_detected:
            cm.tp += 1  # Erreur bien détectée
        elif not is_error and error_detected:
            cm.fp += 1  # Fausse alerte (bonne réponse rejetée)
        elif is_error and not error_detected:
            cm.fn += 1  # Erreur manquée (mauvaise réponse acceptée)
        elif not is_error and not error_detected:
            cm.tn += 1  # Bonne réponse acceptée
    
    return cm


def compute_metrics(cm: ConfusionMatrix) -> Metrics:
    """
    Calcule les métriques à partir de la matrice de confusion.
    
    Args:
        cm: Matrice de confusion
        
    Returns:
        Métriques (précision, recall, F1, spécificité, accuracy)
    """
    total = cm.tp + cm.fp + cm.fn + cm.tn
    
    # Precision: Parmi les erreurs détectées, combien sont réelles ?
    precision = cm.tp / (cm.tp + cm.fp) if (cm.tp + cm.fp) > 0 else 0.0
    
    # Recall (Sensibilité): Parmi les erreurs réelles, combien détectées ?
    recall = cm.tp / (cm.tp + cm.fn) if (cm.tp + cm.fn) > 0 else 0.0
    
    # F1-Score: Moyenne harmonique de précision et recall
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Specificity: Parmi les bonnes réponses, combien acceptées ?
    specificity = cm.tn / (cm.tn + cm.fp) if (cm.tn + cm.fp) > 0 else 0.0
    
    # Accuracy: Proportion de bonnes décisions
    accuracy = (cm.tp + cm.tn) / total if total > 0 else 0.0
    
    return Metrics(
        precision=precision,
        recall=recall,
        f1=f1,
        specificity=specificity,
        accuracy=accuracy
    )


def format_confusion_matrix(cm: ConfusionMatrix) -> str:
    """
    Formate la matrice de confusion pour affichage.
    
    Args:
        cm: Matrice de confusion
        
    Returns:
        String formaté
    """
    total = cm.tp + cm.fp + cm.fn + cm.tn
    
    return (
        f"\n=== Matrice de Confusion ===\n"
        f"TP (Erreur détectée)       : {cm.tp:3d}\n"
        f"FP (Fausse alerte)         : {cm.fp:3d}\n"
        f"FN (Erreur manquée)        : {cm.fn:3d}\n"
        f"TN (Bonne réponse acceptée): {cm.tn:3d}\n"
        f"Total                      : {total:3d}\n"
    )
