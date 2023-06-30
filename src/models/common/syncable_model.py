from src.app import db
from .application_model import ApplicationModel


class SyncableModel(ApplicationModel):
    __abstract__ = True

    identifier = db.Column(db.String(36), nullable=False, index=True, unique=True)

    synced_at = db.Column(db.DateTime(timezone=True))
