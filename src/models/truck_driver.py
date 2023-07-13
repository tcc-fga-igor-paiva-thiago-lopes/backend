import bcrypt
from src.app import db
from sqlalchemy.sql import func

from .common.application_model import ApplicationModel

from .freight import Freight
from .category import Category


class TruckDriver(ApplicationModel):
    __tablename__ = "TRUCK_DRIVER"

    FRIENDLY_NAME_SINGULAR = "Usuário"
    FRIENDLY_NAME_PLURAL = "Usuários"

    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password_digest = db.Column(db.String(512))
    last_sign_in_at = db.Column(db.DateTime(timezone=True))

    freights = db.relationship(Freight, back_populates="truck_driver")
    categories = db.relationship(Category, back_populates="truck_driver")

    def __init__(self, **kwargs):
        password = kwargs.pop("password", None)
        password_confirmation = kwargs.pop("password_confirmation", None)

        if len(password or "") == 0 or len(password_confirmation or "") == 0:
            raise Exception("Password and password confirmation are required")

        password_digest = self._digest_password(password, password_confirmation)

        return super().__init__(**kwargs, password_digest=password_digest)

    def _digest_password(self, password, password_confirmation):
        if password != password_confirmation:
            raise Exception("Password and password confirmation must be equal")

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        return password_hash.decode("utf8")

    def login(self):
        self.last_sign_in_at = func.now()
        self.save()

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_digest.encode("utf-8")
        )
