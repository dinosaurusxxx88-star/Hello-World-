# Simulation: comportements d'IA

Ce répertoire contient un script de démonstration qui simule différents comportements d'une intelligence artificielle et un processus de vérification critique humain.

Fichier principal
- simulation/ia_comportements.py
  - Simule des réponses d'IA (types: `correct`, `confident_mistake`, `hallucination`, `biased`).
  - Fournit une vérification humaine simplifiée (comparaison avec une petite base de connaissances, acceptation par seuil de confiance, détection d'erreurs).
  - CLI: options pour le nombre d'itérations, seed, fichier de questions et sortie JSON.

Prérequis
- Python 3.8+ (le script utilise uniquement la bibliothèque standard).
- (Optionnel) Créez un environnement virtuel :
  - python3 -m venv .venv
  - source .venv/bin/activate  # macOS / Linux
  - .\.venv\Scripts\activate   # Windows (PowerShell)

Exemples d'exécution
- Exécution simple (résumé lisible) :
  python3 simulation/ia_comportements.py

- Exécution reproductible et sortie JSON :
  python3 simulation/ia_comportements.py --runs 300 --seed 42 --json-output

- Utiliser un fichier de questions (questions.json doit contenir une liste JSON de chaînes) :
  python3 simulation/ia_comportements.py --questions-file questions.json

Format du fichier questions.json (exemple)
[
  "Qui a écrit 'Le Petit Prince' ?",
  "Quelle est la capitale de la France ?",
  "2+2 = ?",
  "Explique pourquoi X cause Y.",
  "Donne une méthode pour résoudre un problème éthique."
]

Options CLI (résumé)
- --runs N                Nombre d'itérations (par défaut 300)
- --seed S                Seed pour reproductibilité (optionnel)
- --questions-file PATH   Fichier JSON listant les questions
- --conf-accept-threshold FLOAT  Seuil de confiance pour accepter une réponse marquée "correct" (défaut 0.7)
- --json-output           Afficher la sortie complète en JSON

Sortie
- Par défaut, le script affiche un résumé lisible (statistiques et exemples d'erreurs détectées).
- Avec --json-output, le script renvoie un objet JSON contenant les statistiques et exemples (pratique pour tests et visualisations).

Prochaines suggestions
- Transformer en notebook Jupyter avec graphiques (matplotlib / seaborn) pour visualiser taux d'erreur et détection.
- Ajouter tests unitaires (pytest) pour couvrir la logique de détection et les heuristiques.
- Ajouter un requirements.txt si de nouvelles dépendances sont ajoutées.
- Intégrer des vérifications contre des sources externes ou APIs pour réduire les hallucinations.

Issue associée
- Cette simulation et ses améliorations sont liées à l'issue #3 : https://github.com/dinosaurusxxx88-star/Hello-World-/issues/3

