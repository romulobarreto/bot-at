"""
Consultas ao banco de dados.
"""

import pandas as pd
from src.db.connection import get_connection


def get_cadastro_by_instalacao(instalacao: str) -> pd.DataFrame:
    query = """
        SELECT *
        FROM cadastro
        WHERE TRIM(CAST(INSTALACAO AS TEXT)) = TRIM(?)
    """

    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=[instalacao])


def get_cadastro_by_medidor(medidor: str) -> pd.DataFrame:
    query = """
        SELECT *
        FROM cadastro
        WHERE TRIM(CAST(MEDIDOR AS TEXT)) = TRIM(?)
    """

    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=[medidor])


def get_equipamentos(instalacao: str) -> pd.DataFrame:
    query = """
        SELECT *
        FROM equipamentos
        WHERE TRIM(CAST(INSTALACAO AS TEXT)) = TRIM(?)
    """

    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=[str(instalacao).strip()])


def get_consumo(instalacao: str) -> pd.DataFrame:
    query = """
        SELECT *
        FROM consumo_demanda
        WHERE TRIM(CAST(INSTALACAO AS TEXT)) = TRIM(?)
        ORDER BY MES DESC
        LIMIT 12
    """

    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=[instalacao])
