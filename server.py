from flask.cli import FlaskGroup
from src.app import create_app, db

if __name__ == "__main__":
    # app, _, _ = create_app()
    app = create_app()

    app.run(host="0.0.0.0", debug=True)

    # with app.app_context():
        # db.create_all()
        # db.session.commit()

    # cli = FlaskGroup(app)

    # @cli.command("create_db")
    # def create_db():
    #     db.drop_all()
    #     db.create_all()
    #     db.session.commit()


    # @cli.command("seed_db")
    # def seed_db():
    #     db.session.add(
    #         TruckDriver(
    #             name="John",
    #             email="john@mail.com",
    #             password="password123",
    #             password_confirmation="password123"
    #         )
    #     )
    #     db.session.commit()

# from src.app import app

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True)
