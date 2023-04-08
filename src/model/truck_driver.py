import bcrypt
from src.app import db
from sqlalchemy.sql import func
from .application_model import ApplicationModel


class TruckDriver(db.Model, ApplicationModel):
    __tablename__ = "TRUCK_DRIVER"

    FRIENDLY_NAME_SINGULAR = "Usuário"
    FRIENDLY_NAME_PLURAL = "Usuários"

    id = db.Column(db.Integer, db.Identity(start=1, cycle=True), primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password_digest = db.Column(db.String(512))
    last_sign_in_at = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, name, email, password, password_confirmation, last_sign_in_at=None):
        self.name = name
        self.email = email
        self.last_sign_in_at = last_sign_in_at
        self.password_digest = self.digest_password(password, password_confirmation)

    def digest_password(self, password, password_confirmation):
        if password != password_confirmation:
            raise Exception('Password and password confirmation must be equal')

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        return password_hash.decode('utf8')

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password_digest.encode("utf-8")
        )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "last_sign_in_at": str(self.last_sign_in_at),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
