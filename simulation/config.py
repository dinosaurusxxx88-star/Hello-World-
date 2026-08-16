# simulation/config.py
# Configuration centralisée pour la simulation de comportements IA

# Distribution des types d'erreurs IA (doit sommer à 1.0)
DEFAULT_ERROR_DISTRIBUTION = {
    "correct": 0.6,
    "confident_mistake": 0.2,
    "hallucination": 0.15,
    "biased": 0.05,
}

# Plages de confiance par type de réponse
CONFIDENCE_RANGES = {
    "correct": (0.7, 1.0),
    "confident_mistake": (0.85, 1.0),
    "hallucination": (0.6, 0.95),
    "biased": (0.5, 0.9),
}

# Seuil par défaut pour accepter une réponse marquée "correct"
DEFAULT_CONFIDENCE_THRESHOLD = 0.7

# Chemin par défaut pour la base de connaissances
DEFAULT_KB_PATH = "simulation/data/knowledge_base.json"

# Chemin par défaut pour les questions
DEFAULT_QUESTIONS_PATH = "simulation/data/questions.json"

# Nombre par défaut d'itérations de simulation
DEFAULT_RUNS = 300
