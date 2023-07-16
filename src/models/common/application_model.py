from src.app import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import insert as postgresql_upsert


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

    @classmethod
    def upsert(cls, data, unique_by):
        upsert_statement = postgresql_upsert(cls).values(data)

        update_columns = {
            col.name: col
            for col in upsert_statement.excluded
            if col.name not in ("id", "created_at", "updated_at")
        }

        upsert_statement = upsert_statement.on_conflict_do_update(
            index_elements=unique_by, set_=update_columns
        ).returning(cls.identifier)

        upserted_identifiers = list(db.session.execute(upsert_statement).scalars())

        db.session.commit()

        return upserted_identifiers

    @classmethod
    def destroy_by_identifiers(cls, identifiers, user):
        delete_statement = (
            db.delete(cls)
            .where(
                cls.identifier.in_(identifiers),
                cls.truck_driver == user,
            )
            .returning(cls.identifier)
        )

        deleted_identifiers = list(db.session.execute(delete_statement).scalars())

        db.session.commit()

        return deleted_identifiers

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
