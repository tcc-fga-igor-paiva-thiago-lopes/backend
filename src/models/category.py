from src.app import db
from sqlalchemy import LargeBinary
from src.models.common.syncable_model import SyncableModel


class Category(SyncableModel):
    __tablename__ = "CATEGORY"

    FRIENDLY_NAME_SINGULAR = "Categoria"
    FRIENDLY_NAME_PLURAL = "Categorias"

    name = db.Column(db.String(60), nullable=False, unique=True)
    color = db.Column(db.String(7), nullable=False)

    truck_driver_id = db.Column(
        db.BigInteger,
        db.ForeignKey("TRUCK_DRIVER.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    truck_driver = db.relationship("TruckDriver", back_populates="categories")

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)
