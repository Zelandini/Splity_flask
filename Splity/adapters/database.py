from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        from Splity.adapters.orm import UserORM, BillORM, BillParticipantORM, GroupORM, RepaymentORM
        db.create_all()
