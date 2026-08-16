# simulation/__init__.py
# Package simulation - Simule comportements IA et vérification critique humaine

__version__ = "1.0.0"
__author__ = "AI Simulation Project"

from .ia_comportements import Response, ai_answer, simulate
from .human_verification import human_critical_check, load_knowledge_base
from .metrics import ConfusionMatrix, Metrics, compute_confusion_matrix, compute_metrics

__all__ = [
    "Response",
    "ai_answer",
    "simulate",
    "human_critical_check",
    "load_knowledge_base",
    "ConfusionMatrix",
    "Metrics",
    "compute_confusion_matrix",
    "compute_metrics",
]
