"""
Serviços relacionados ao cadastro.
"""

from src.db.queries import (
    get_cadastro_by_instalacao,
    get_cadastro_by_medidor,
)


def buscar_por_instalacao(instalacao: str):
    df = get_cadastro_by_instalacao(instalacao)

    if df.empty:
        return None

    return df.iloc[0]


def buscar_por_medidor(medidor: str):
    df = get_cadastro_by_medidor(medidor)

    if df.empty:
        return None

    return df.iloc[0]