"""
Serviços relacionados ao consumo/demanda.
"""

from src.db.queries import get_consumo


def buscar_consumo(instalacao: str):
    df = get_consumo(instalacao)

    if df.empty:
        return None

    return df