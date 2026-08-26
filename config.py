import os
class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY") or "development-only-change-before-deployment"
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL") or "sqlite:///splity.db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    GOOGLE_CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET=os.environ.get("GOOGLE_CLIENT_SECRET")
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE="Lax"
