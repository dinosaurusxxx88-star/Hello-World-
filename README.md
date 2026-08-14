# Hello-World - Simulation IA / vérification humaine

## Description
Simulateur simple d'interactions IA / humain pour tester erreurs, hallucinations et détections.

## Prérequis
- Python 3.8+

## Installation
```bash
git clone https://github.com/dinosaurusxxx88-star/Hello-World-.git
cd Hello-World-
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
```bash
python simulation/ia_comportements.py --runs 200
```

Options utiles :
- `--json-output <fichier>`  Sauvegarde les résultats en JSON
- `--seed <n>`               Seed pour reproductibilité

## Développement / Tests
```bash
pip install -r requirements-dev.txt
pytest
```

## Structure importante
- `simulation/ia_comportements.py` : script principal
- `simulation/README.md` : documentation détaillée de la simulation

## Contribuer
Fork + PR. Écrire des tests pour les fonctions `ai_answer`, `human_critical_check`, `simulate`.

## Licence
MIT
