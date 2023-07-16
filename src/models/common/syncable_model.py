from src.app import db
from .application_model import ApplicationModel


class SyncableModel(ApplicationModel):
    __abstract__ = True

    identifier = db.Column(db.String(36), nullable=False, index=True, unique=True)

    synced_at = db.Column(db.DateTime(timezone=True))

    @classmethod
    def identifier_to_id(cls, user):
        return dict(
            map(
                lambda record: (record.identifier, record.id),
                db.session.execute(
                    db.select(cls).where(cls.truck_driver == user)
                ).scalars(),
            ),
        )
