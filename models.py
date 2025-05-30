from sqlalchemy import (
    Column, Integer, String, Float,
    DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"
    id           = Column(String, primary_key=True)
    name         = Column(String, nullable=False)
    symbol       = Column(String, nullable=False)
    rank         = Column(Integer)
    priceUsd     = Column(Float)
    marketCapUsd = Column(Float)

    history = relationship("AssetHistory", back_populates="asset")

class AssetHistory(Base):
    __tablename__ = "asset_history"
    id           = Column(Integer, primary_key=True, autoincrement=True)
    asset_id     = Column(String, ForeignKey("assets.id"), nullable=False)
    time         = Column(DateTime, nullable=False)
    priceUsd     = Column(Float)
    volumeUsd24h = Column(Float)
    marketCapUsd = Column(Float)

    __table_args__ = (
        UniqueConstraint("asset_id", "time", name="uix_asset_time"),
    )

    asset = relationship("Asset", back_populates="history")