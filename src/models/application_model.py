from src.app import db
from sqlalchemy.sql import func


class ApplicationModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, db.Identity(start=1, cycle=True), primary_key=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)

        instance.save()

        return instance

    @classmethod
    def columns(cls):
        return [col.name for col in list(cls.__table__.columns)]

    def set_attrs(self, **kwargs):
        columns = self.__class__.columns()

        for key, value in kwargs.items():
            if key in columns:
                self.__setattr__(key, value)

    def save(self):
        if self.id is None:
            db.session.add(self)

        return db.session.commit()

    def update(self, **kwargs):
        self.set_attrs(**kwargs)

        return self.save()

    def destroy(self):
        db.session.delete(self)

        return db.session.commit()

    def reload(self):
        db.session.refresh(self)
