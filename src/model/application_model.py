from src.app import db


class ApplicationModel:
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)

        instance.save()

        return instance

    def set_attrs(self, **kwargs):
        for key, value in kwargs.items():
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
