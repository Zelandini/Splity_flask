from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    print(">>> init_db called!")  # ADD THIS
    db.init_app(app)

    from Splity.adapters import orm
    print(">>> ORM models imported!")  # ADD THIS

    with app.app_context():
        print(">>> Creating tables...")  # ADD THIS
        db.create_all()
        print(">>> Tables created!")  # ADD THIS