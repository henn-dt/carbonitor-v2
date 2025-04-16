# app/infrastructure/infrastructure/services/password_service.py
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.application.services.ipassword_service import IPasswordService

class PasswordService(IPasswordService):
    def hash_password(self, plain_password: str) -> str:
        return generate_password_hash(plain_password, method='pbkdf2:sha256')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, plain_password)