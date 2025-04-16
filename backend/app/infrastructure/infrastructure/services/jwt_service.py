# app/infrastructure/services/jwt_service.py
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple
import jwt
from jwt import exceptions as jwt_exceptions
from app.core.application.services.ijwt_service import IJWTService

class JWTService(IJWTService):
    def __init__(
        self,
        secret_key: str,
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 7,
        algorithm: str = "HS256"
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_token_expire_minutes = access_token_expire_minutes
        self._refresh_token_expire_days = refresh_token_expire_days

    def _create_token(self, data: Dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        
        # Add standard JWT claims
        now = datetime.now(timezone.utc)
        to_encode.update({
            "iat": now,  # Issued at
            "exp": now + expires_delta,  # Expiration
            "nbf": now,  # Not valid before
        })
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def create_access_token(self, user_id: int, permissions: list[str], additional_claims: Dict = None) -> Tuple[str, datetime]:
        claims = {
            "sub": str(user_id),
            "type": "access",
            "permissions": permissions
        }
        if additional_claims:
            claims.update(additional_claims)

        expires_delta = timedelta(minutes=self._access_token_expire_minutes)
        expire_time = datetime.now(timezone.utc) + expires_delta
        token = self._create_token(claims, expires_delta)
        
        return token, expire_time

    def create_refresh_token(self, user_id: int, token_id: str) -> Tuple[str, datetime]:
        claims = {
            "sub": str(user_id),
            "type": "refresh",
            "jti": token_id  # JWT ID for token tracking
        }
        
        expires_delta = timedelta(days=self._refresh_token_expire_days)
        expire_time = datetime.now(timezone.utc) + expires_delta
        token = self._create_token(claims, expires_delta)
        
        return token, expire_time

    def validate_token(self, token: str, verify_type: Optional[str] = None) -> Dict:
        try:
            payload = jwt.decode(
                token, 
                self._secret_key, 
                algorithms=[self._algorithm],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "verify_iat": True,
                    "require": ["exp", "iat", "nbf", "sub", "type"]
                }
            )
            
            # Verify token type if requested
            if verify_type and payload.get("type") != verify_type:
                raise ValueError(f"Invalid token type. Expected {verify_type}")
            
            return payload
        except jwt_exceptions.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt_exceptions.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    def validate_access_token(self, token: str) -> Dict:
        return self.validate_token(token, verify_type="access")

    def validate_refresh_token(self, token: str) -> Dict:
        return self.validate_token(token, verify_type="refresh")

    def get_token_expiration(self, token: str) -> datetime:
        payload = self.validate_token(token)
        return datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    def get_user_id_from_token(self, token: str) -> int:
        payload = self.validate_token(token)
        return int(payload["sub"])

    def get_token_id(self, token: str) -> Optional[str]:
        payload = self.validate_token(token)
        return payload.get("jti")
    
    def get_permissions_from_token(self, token: str) -> list[str]:
        payload = self.validate_token(token)
        return payload.get("permissions", [])