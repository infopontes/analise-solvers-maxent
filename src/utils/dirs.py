# src/utils/dirs.py
import os

def ensure_dirs(*dirs):
    """
    Cria as pastas se não existirem.
    """
    for d in dirs:
        os.makedirs(d, exist_ok=True)
