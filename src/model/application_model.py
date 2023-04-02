from src.app import db


class ApplicationModel:
    @classmethod
    def create(klass, **kwargs):
        instance = klass(**kwargs)

        instance.save()

        return instance

    def save(self):
        if self.id is None:
            db.session.add(self)

        return db.session.commit()

    def destroy(self):
        db.session.delete(self)

        return db.session.commit()
