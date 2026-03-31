# Reinitialiser le projet depuis le repo Git

Ce guide couvre uniquement la remise a zero de l'environnement local a partir du depot.

## 1 Prerequis

- Git installe
- Python 3.12+
- `uv` installe

## 2 Cloner le projet

```bash
git clone https://github.com/CorentinFERRY/skills-manager.git
cd skills_manager
```

## 3 Installer `uv`

Linux / macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verifier l'installation:

```bash
uv --version
```

## 4 Installer les dependances du projet

Depuis la racine du repo:

```bash
uv add fastapi                           
uv add --dev pytest pytest-cov mypy ruff 
```
Cette commande installe:

- dependances applicatives (ex: `fastapi`)
- dependances de developpement (pytest, ruff, mypy, etc.)

## 5 Configuration ruff & pytest

```TOML
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I"]

[tool.pytest.ini_options]
pythonpath = ["src/skills-manager"]
testpaths = ["tests"]
addopts = "--cov=. --cov-fail-under=80"
```


## 6 Verifier que tout est OK

Lancer les tests:

```bash
uv run pytest
```

Lancer le script principal:

```bash
uv run python src/skills_manager/main.py
```

## 7 Importer les File Watchers (PyCharm)

```
Settings -> Tools -> File Watchers -> import -> watchers.xml
```

Permet d'importer ruff check --fix et ruff format et de les executer à la sauvegarde manuelle 