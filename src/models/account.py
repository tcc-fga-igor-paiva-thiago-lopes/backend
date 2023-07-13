from src.app import db

from .common.syncable_model import SyncableModel


class Account(SyncableModel):
    __tablename__ = "ACCOUNT"

    FRIENDLY_NAME_SINGULAR = "Conta"
    FRIENDLY_NAME_PLURAL = "Contas"

    name = db.Column(db.String(30), nullable=False)
    value = db.Column(db.Numeric(8, 2), nullable=False)
    account_date = db.Column(db.DateTime(timezone=False))
    description = db.Column(db.String(500), nullable=False)

    freight_id = db.Column(
        db.BigInteger,
        db.ForeignKey("FREIGHT.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    freight = db.relationship("Freight", back_populates="accounts")
