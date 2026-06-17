from src.db.queries import get_cadastro_by_instalacao


def buscar_coordenadas(instalacao: str):
    df = get_cadastro_by_instalacao(instalacao)

    if df.empty:
        return None, None

    row = df.iloc[0]

    lat = row.get("LATITUDE")
    lon = row.get("LONGITUDE")

    if lat is None or lon is None:
        return None, None

    return lat, lon