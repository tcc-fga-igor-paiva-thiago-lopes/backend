import enum

from src.app import db

from .application_model import ApplicationModel


class FreightCargoEnum(str, enum.Enum):
    GENERAL = "Geral"
    CONTAINERIZED = "Conteinerizada"
    REFRIGERATED = "Frigorificada"
    LIQUID_BULK = "Granel Líquido"
    PRESSURIZED_BULK = "Granel Pressurizada"
    SOLID_BULK = "Granel Sólido"
    NEW_BULK = "Neogranel"
    DANGER = "Frigorificada"
    DANGEROUS_GENERAL = "Perigosa Geral"
    DANGEROUS_CONTAINERIZED = "Perigosa Conteinerizada"
    DANGEROUS_REFRIGERATED = "Perigosa Frigorificada"
    DANGEROUS_LIQUID_BULK = "Perigosa Granel Líquido"
    DANGEROUS_PRESSURIZED_BULK = "Perigosa Granel Pressurizada"
    DANGEROUS_SOLID_BULK = "Perigosa Granel Sólido"


class FreightStatusEnum(str, enum.Enum):
    NOT_STARTED = ("Não iniciado",)
    STARTED = ("Em progresso",)
    WAITING_UNLOAD = ("Aguardando descarga",)
    # WAITING_PAYMENT = 'Aguardando pagamento',
    FINISHED = ("Finalizado",)


class Freight(ApplicationModel):
    __tablename__ = "FREIGHT"

    FRIENDLY_NAME_SINGULAR = "Frete"
    FRIENDLY_NAME_PLURAL = "Fretes"

    cargo = db.Column(db.Enum(FreightCargoEnum), nullable=False)
    status = db.Column(db.Enum(FreightStatusEnum), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    contractor = db.Column(db.String(60), nullable=False)
    cargo_weight = db.Column(db.Numeric(8, 2), nullable=False)
    agreed_payment = db.Column(db.Numeric(8, 2), nullable=False)
    distance = db.Column(db.Numeric(8, 2), nullable=False)

    start_date = db.Column(db.DateTime(timezone=True))
    due_date = db.Column(db.DateTime(timezone=True))
    finished_date = db.Column(db.DateTime(timezone=True))

    origin_city = db.Column(db.String(50), nullable=False)
    origin_state = db.Column(db.CHAR(2), nullable=False)
    origin_country = db.Column(db.String(50))
    origin_latitude = db.Column(db.Numeric(9, 6))
    origin_longitude = db.Column(db.Numeric(9, 6))

    destination_city = db.Column(db.String(50), nullable=False)
    destination_state = db.Column(db.CHAR(2), nullable=False)
    destination_country = db.Column(db.String(50))
    destination_latitude = db.Column(db.Numeric(9, 6))
    destination_longitude = db.Column(db.Numeric(9, 6))

    truck_driver_id = db.Column(
        db.BigInteger,
        db.ForeignKey("TRUCK_DRIVER.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    truck_driver = db.relationship("TruckDriver", back_populates="freights")
