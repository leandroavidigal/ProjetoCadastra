import pandas as pd
from sqlalchemy import text
from db import engine

def get_assets(limit=20):
    query = f"SELECT * FROM assets ORDER BY marketCapUsd DESC LIMIT {limit}"
    return pd.read_sql_query(query, engine)

def get_asset_history(asset_id):
    query = text("""
        SELECT time, priceUsd, volumeUsd24h, marketCapUsd
        FROM asset_history
        WHERE asset_id = :asset
        ORDER BY time
    """)
    return pd.read_sql_query(query, engine, params={"asset": asset_id})

def get_all_asset_ids():
    df = pd.read_sql("SELECT id, name FROM assets ORDER BY name", engine)
    return df
