from src.app import db
from sqlalchemy import LargeBinary
from .application_model import ApplicationModel


class Category(ApplicationModel):
    __tablename__ = "CATEGORY"

    FRIENDLY_NAME_SINGULAR = "Categoria"
    FRIENDLY_NAME_PLURAL = "Categorias"

    name = db.Column(db.String(60), nullable=False, unique=True)
    color = db.Column(LargeBinary, nullable=False)

    def __init__(self, **kwargs):
        color = kwargs.pop("color", None)

        if len(color or "") == 0:
            raise Exception("Color is required")

        color = bytes.fromhex(color)

        return super().__init__(**kwargs, color=color)

    def get_color(self):
        return self.color.hex()
