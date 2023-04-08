from src.app import db


class ApplicationModel:
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)

        instance.save()

        return instance

    def save(self):
        if self.id is None:
            db.session.add(self)

        return db.session.commit()

    def update(self, attributes):
        # don't know why there is no option to update using model instance
        self.__class__.query.filter_by(id=self.id).update(attributes)

        return db.session.commit()

    def destroy(self):
        db.session.delete(self)

        return db.session.commit()
