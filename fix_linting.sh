#!/bin/bash

# Script pour corriger les problèmes de linting automatiquement

echo "=== Correction automatique du code ==="

# 1. Correction des bare except
echo "Correction des 'bare except'..."

# Trouver et corriger les bare except
find . -name "*.py" -type f -exec grep -l "except:" {} \; | while read file; do
    echo "Correction de $file"
    # Remplacer bare except par except Exception:
    sed -i 's/^\([[:space:]]*\)except:$/\1except Exception:/g' "$file"
    # Remplacer bare except avec espace
    sed -i 's/except:$/except Exception:/g' "$file"
done

# 2. Formater avec ruff
echo "Formatage avec ruff..."
uv run ruff check --fix .
uv run ruff format .

# 3. Lancer pre-commit
echo "Lancement de pre-commit..."
uv run pre-commit run --all-files

echo "=== Correction terminée ==="
