from src.app import db

class ApplicationModel:
    def save(self):
        if self.id == None:
            db.session.add(self)
            
        return db.session.commit()

    def destroy(self):
        db.session.delete(self)

        return db.session.commit()
