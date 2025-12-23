from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

    with app.app_context():
        # Import inside context to register models to this specific 'db' instance
        from Splity.adapters.orm import UserORM, BillORM, BillParticipantORM, GroupORM
        # Verification print
        print(f">>> Tables in registry: {list(db.metadata.tables.keys())}")
        db.create_all()
        print(">>> Database initialized!")