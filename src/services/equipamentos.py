"""
Serviços relacionados a equipamentos.
"""

from src.db.queries import get_equipamentos


def buscar_equipamentos(instalacao: str):
    df = get_equipamentos(instalacao)

    if df.empty:
        return []

    return df.to_dict(orient="records")