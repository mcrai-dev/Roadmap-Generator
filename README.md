# Générateur IA de Diagrammes

Ce projet permet de générer des diagrammes (UML, mindmap, organigramme, etc.) à partir d'une description textuelle en français, grâce à l'IA (OpenAI) et à Graphviz.

## Structure du projet

- `backend/` : API Flask pour générer le code Graphviz (DOT) et le diagramme SVG.
  - `main.py` : Point d'entrée de l'API (Flask), logique de génération.
  - `prompts.py` : Prompts utilisés pour guider l'IA selon le type de diagramme.
- `frontend/` : Interface web pour interagir avec l'utilisateur.
  - `index.html` : Interface utilisateur moderne, permet d'envoyer une requête à l'API et d'afficher le diagramme généré.
- `app-v3.py` : Script autonome pour générer un diagramme via la console (hors API).
- `prompts.py` : Prompts pour le script autonome.
- `.env` : Fichier de configuration de la clé OpenAI (non fourni).

## Installation

1. **Cloner le dépôt**
2. Créer un environnement virtuel :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Ajouter votre clé OpenAI dans un fichier `.env` :
   ```env
   OPENAI_API_KEY=sk-xxxxxx
   ```

## Lancement de l'API (backend)

```bash
cd backend
python main.py
```

L'API sera accessible sur http://127.0.0.1:5000

## Lancement du frontend

Ouvrir `frontend/index.html` dans un navigateur.

## Utilisation du script autonome

```bash
python app-v3.py
```

## Fonctionnalités principales
- Génération de diagrammes à partir de texte en français
- Types supportés : diagramme de classes UML, organigramme, carte mentale, graphe relationnel
- Interface web moderne (zoom, export PNG, centrage)

## Dépendances principales
- Flask, Flask-CORS, python-dotenv, OpenAI, Graphviz (Python)
- HTML/CSS/JS (frontend)

## Remarques
- La clé OpenAI n'est pas incluse.
- Graphviz doit être installé sur votre système (https://graphviz.gitlab.io/download/).
- Pour la production, adapter la sécurité de l'API et le déploiement.
