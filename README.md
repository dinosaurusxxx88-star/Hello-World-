# Hello-World- 🤖

Projet d'étude et simulation du comportement d'une **Intelligence Artificielle** avec système de **vérification critique humaine**.

## 📋 Description

Ce projet contient :

1. **`simulation/`** - Module de simulation des comportements d'IA
   - Simule différents types de réponses : correctes, erreurs confiantes, hallucinations, biais
   - Implémente une vérification critique simplifiée par l'humain
   - Collecte des statistiques pour analyser la détection d'erreurs

2. **`tests/`** - Suite de tests unitaires complets
   - Tests des fonctions principales avec pytest
   - Couvre les cas normaux, limites et d'intégration

## 🚀 Démarrage rapide

### Prérequis

- **Python 3.8+** (utilise uniquement la bibliothèque standard)
- (Optionnel) Environnement virtuel :
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate  # macOS / Linux
  .\.venv\Scripts\activate   # Windows (PowerShell)
  ```

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/dinosaurusxxx88-star/Hello-World-.git
cd Hello-World-

# Installer les dépendances (pytest pour les tests)
pip install -r requirements.txt
```

### Exécution

#### Lancer la simulation

```bash
# Exécution simple avec résumé lisible
python3 simulation/ia_comportements.py

# Exécution avec options
python3 simulation/ia_comportements.py --runs 300 --seed 42 --json-output

# Utiliser un fichier de questions personnalisé
python3 simulation/ia_comportements.py --questions-file questions.json
```

#### Options disponibles

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--runs` | int | 300 | Nombre d'itérations |
| `--seed` | int | None | Seed pour reproductibilité |
| `--questions-file` | str | None | Fichier JSON avec questions |
| `--conf-accept-threshold` | float | 0.7 | Seuil de confiance pour accepter |
| `--json-output` | flag | False | Sortie en JSON |

#### Lancer les tests

```bash
# Tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/test_ia_comportements.py::TestAiAnswer -v

# Avec rapport de couverture
pytest tests/ --cov=simulation
```

## 📁 Structure du projet

```
Hello-World-/
├── simulation/
│   ├── __init__.py
│   ├── ia_comportements.py      # Module principal
│   ├── config.py                # Configuration
│   ├── human_verification.py    # Vérification humaine
│   ├── metrics.py               # Métriques
│   └── README.md                # Documentation détaillée
├── tests/
│   ├── __init__.py
│   └── test_ia_comportements.py # Suite de tests complète
├── requirements.txt
└── README.md
```

## 🧪 Fonctionnalités principales

### Simulation d'IA (`simulation/ia_comportements.py`)

La simulation génère 4 types de réponses :

- **`correct`** (60%) : Réponses exactes ou plausibles
- **`confident_mistake`** (20%) : Erreurs malgré une haute confiance
- **`hallucination`** (15%) : Faits inventés ou faux
- **`biased`** (5%) : Réponses stéréotypées ou orientées

### Vérification critique humaine

L'humain vérifie chaque réponse en :
- Comparant contre une base de connaissances
- Vérifiant la confiance déclarée
- Détectant hallucinations et biais
- Demandant sources si nécessaire

### Statistiques et résultats

```json
{
  "stats": {
    "total": 300,
    "errors": 120,
    "detected_errors": 115
  },
  "examples": [
    {
      "q": "Qui a écrit 'Le Petit Prince' ?",
      "ai": {
        "type": "hallucination",
        "text": "Selon le rapport X...",
        "conf": 0.75
      },
      "check": "Pas de source, ressemble à une hallucination."
    }
  ]
}
```

## 📊 Tests

La suite de tests couvre :

- ✅ Normalisation des chaînes
- ✅ Génération de réponses simulées
- ✅ Vérification critique des réponses
- ✅ Orchestration complète
- ✅ Cas limites et intégration

**Coverage** : ~95% du code principal

Exécuter les tests :
```bash
pytest tests/ -v --cov=simulation
```

## 📝 Format des fichiers de questions

### questions.json

```json
[
  "Qui a écrit 'Le Petit Prince' ?",
  "Quelle est la capitale de la France ?",
  "2+2 = ?",
  "Explique pourquoi X cause Y.",
  "Donne une méthode pour résoudre un problème éthique."
]
```

## 🔧 Développement

### Ajouter de nouvelles dépendances

Si vous ajoutez des dépendances au projet, mettez à jour `requirements.txt` :

```bash
pip freeze > requirements.txt
```

### Exécuter les tests après modifications

```bash
# Tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=simulation --cov-report=html
```

## 📚 Ressources et améliorations futures

### Suggestions d'améliorations

- [ ] Transformer en notebook Jupyter avec visualisations (matplotlib/seaborn)
- [ ] Intégrer des vérifications contre des sources externes (APIs)
- [ ] Ajouter des modèles LLM réels (OpenAI, Anthropic, Ollama)
- [ ] Créer une interface web interactive
- [ ] Ajouter métriques plus sophistiquées (ROC, confusion matrix)

### Issues liées

- [Issue #3](https://github.com/dinosaurusxxx88-star/Hello-World-/issues/3) : Comportements d'IA
- [Issue #4](https://github.com/dinosaurusxxx88-star/Hello-World-/issues/4) : Implémentation détaillée

## 📖 Documentation complète

Voir [`simulation/README.md`](simulation/README.md) pour la documentation détaillée du module de simulation.

## 🤝 Contribution

Les contributions sont bienvenues ! Merci de :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.

## 👤 Auteur

**dinosaurusxxx88-star**

---

**Dernier update** : 2026-08-16  
**Status** : ✅ Tests CI/CD opérationnels
