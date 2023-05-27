from src.app import db

# Must import, so the relationship is loaded properly
from .truck_driver import TruckDriver
from .application_model import ApplicationModel


class Freight(ApplicationModel):
    __tablename__ = "FREIGHT"

    FRIENDLY_NAME_SINGULAR = "Frete"
    FRIENDLY_NAME_PLURAL = "Fretes"

    cargo = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    contractor = db.Column(db.String(60), nullable=False)
    cargo_weight = db.Column(db.Numeric(8, 2), nullable=False)
    agreed_payment = db.Column(db.Numeric(8, 2), nullable=False)
    distance = db.Column(db.Numeric(8, 2), nullable=False)

    start_date = db.Column(db.DateTime(timezone=True), nullable=False)
    due_date = db.Column(db.DateTime(timezone=True))
    finished_date = db.Column(db.DateTime(timezone=True))

    origin_city = db.Column(db.String(50))
    origin_state = db.Column(db.CHAR(2))
    origin_country = db.Column(db.String(50))
    origin_latitude = db.Column(db.Numeric(9, 6))
    origin_longitude = db.Column(db.Numeric(9, 6))

    destination_city = db.Column(db.String(50))
    destination_state = db.Column(db.CHAR(2))
    destination_country = db.Column(db.String(50))
    destination_latitude = db.Column(db.Numeric(9, 6))
    destination_longitude = db.Column(db.Numeric(9, 6))

    truck_driver_id = db.Column(
        db.BigInteger,
        db.ForeignKey("TRUCK_DRIVER.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    truck_driver = db.relationship(TruckDriver, back_populates="freights")
