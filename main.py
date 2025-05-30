import logging
import requests
from datetime import datetime
from api_client import CoinCapClient
from db import SessionLocal, engine
from models import Base, Asset, AssetHistory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    Base.metadata.create_all(bind=engine)

def upsert_asset(session, data):
    # tenta buscar; se não existir, cria um novo Asset
    a = session.get(Asset, data["id"]) or Asset(id=data["id"])

    # campos obrigatórios
    a.name   = data["name"]
    a.symbol = data["symbol"]
    a.rank   = int(data.get("rank") or 0)

    # trata priceUsd (pode ser None)
    price = data.get("priceUsd")
    a.priceUsd = float(price) if price is not None else None

    # trata marketCapUsd (pode ser None)
    mcap = data.get("marketCapUsd")
    a.marketCapUsd = float(mcap) if mcap is not None else None

    session.merge(a)

def insert_history(session, slug):
    # se slug for vazio ou None, pule
    if not slug:
        logger.warning(f"Slug vazio, pulando histórico.")
        return

    client = CoinCapClient()
    try:
        history = client.fetch_asset_history(slug)
    except requests.HTTPError as e:
        # se der 404 ou outro erro de HTTP, logue e pule
        logger.warning(f"Não foi possível obter histórico de '{slug}': {e}")
        return

    for h in history:
        # mesmo bloco de antes, inserindo cada registro
        dt = datetime.fromtimestamp(int(h["time"]) / 1000)
        rec = AssetHistory(
            asset_id     = slug,
            time         = dt,
            priceUsd     = float(h.get("priceUsd", 0)),
            volumeUsd24h = float(h.get("volumeUsd24Hr", 0)),
            marketCapUsd = float(h.get("marketCapUsd", 0)),
        )
        try:
            session.add(rec)
            session.flush()
        except Exception:
            session.rollback()
        else:
            session.commit()

def main():
    init_db()
    sess   = SessionLocal()
    client = CoinCapClient()

    # 1) Paginando assets
    offset = 0
    while True:
        assets = client.fetch_assets(offset=offset)
        if not assets: break
        for a in assets:
            upsert_asset(sess, a)
        sess.commit()
        offset += len(assets)

    # 2) Histórico de cada asset
    slugs = [r[0] for r in sess.query(Asset.id).all()]
    for slug in slugs:
        logger.info(f"Inserindo histórico de {slug}...")
        insert_history(sess, slug)

if __name__ == "__main__":
    main()