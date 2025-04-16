# app/infrastructure/services/authentication_service.py
import uuid
from app.core.application.services.iauthentication_service import IAuthenticationService
from app.core.application.services.iuser_service import IUserService
from app.core.application.services.irole_service import IRoleService
from app.core.application.services.iuser_roles_service import IUserRolesService
from app.core.application.services.ijwt_service import IJWTService
from app.core.application.services.ipassword_service import IPasswordService
from app.core.application.dtos.auth.login_dto import LoginDTO
from app.core.application.dtos.auth.register_dto import RegisterDTO
from app.core.application.dtos.auth.auth_response_dto import AuthResponseDTO
from app.core.application.dtos.user.create_user_dto import CreateUserDTO
from app.core.application.dtos.user_roles.user_roles_dto import UserRolesRoleDTO, UserRolesUserDTO
from app.config import Config
from app.core.application.dtos.user_roles.create_user_roles_dto import AssignRoleToUserDTO

class AuthenticationService(IAuthenticationService):
    def __init__(
        self,
        user_service: IUserService,
        role_service: IRoleService,
        user_roles_service: IUserRolesService,
        jwt_service: IJWTService,
        password_service: IPasswordService,
    ):
        self._user_service = user_service
        self._role_service = role_service
        self._user_roles_service = user_roles_service
        self._jwt_service = jwt_service
        self._password_service = password_service
        

    # mappers  auth registerDTO to createUserDTO,     
    def register(self, dto: RegisterDTO) -> AuthResponseDTO:
        # Validate passwords match
        if dto.password != dto.confirm_password:
            raise ValueError("Passwords do not match")
        # Create user and user roles
        user = self._user_service.create_user(CreateUserDTO(email=dto.email,username=dto.username,password=dto.password))
        role = self._role_service.get_role_by_name(Config.USER_CONFIG.DEFAULT_USER_ROLE_NAME)
        assign_dto = AssignRoleToUserDTO(user=UserRolesUserDTO(id=user.id),role=UserRolesRoleDTO(id=role.id))
        self._user_roles_service.assign_role_to_user(assign_dto)
        # Get user roles and permissions
        user_roles = self._user_roles_service.get_roles_by_user(UserRolesUserDTO(id=user.id))
        # Create tokens
        return self._create_auth_response(user.id, user.username, user.email, list(user_roles.permissions))
        
    def login(self, dto: LoginDTO) -> AuthResponseDTO:
        # Get user by email or username
        user = None
        if dto.email_or_username:
            user = self._user_service.get_user_by_email(dto.email_or_username)
            if not user:
                user = self._user_service.get_user_by_username(dto.email_or_username)
        if not user:
            raise ValueError("Invalid email or username")
        # Verify password
        hashed_password = self._user_service.get_user_password(user.id)
        if not self._password_service.verify_password(dto.password, hashed_password):
            raise ValueError("Invalid password")
        # Check if user is active
        user_profile = self._user_service.get_user_profile(user.id)
        if not user_profile.is_active:
            raise ValueError("User account is inactive")
        # Get user roles and permissions
        user_roles = self._user_roles_service.get_roles_by_user(UserRolesUserDTO(id=user.id))
        # Create tokens
        return self._create_auth_response(user.id, user.username, user.email, list(user_roles.permissions))
    
    def refresh_token(self, refresh_token: str) -> AuthResponseDTO:
        # Validate refresh token
        payload = self._jwt_service.validate_refresh_token(refresh_token)
        user_id = int(payload["sub"])
        token_id = payload.get("jti")
        if not token_id:
            raise ValueError("Invalid refresh token")
        # Get user
        user = self._user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        # Check if user is active
        user_profile = self._user_service.get_user_profile(user_id)
        if not user_profile.is_active:
            raise ValueError("User account is inactive")
        # Get user roles and permissions
        user_roles = self._user_roles_service.get_roles_by_user(UserRolesUserDTO(id=user_id))
        # Create new tokens
        return self._create_auth_response(user.id, user.username, user.email, list(user_roles.permissions))
    
    def logout(self, user_id: int) -> None:
        self._user_service.update_user_system(user_id, {"token_revoked": True})
    
    def _create_auth_response(self, user_id: int, username: str, email: str, permissions: list[str]) -> AuthResponseDTO:
        token_id = str(uuid.uuid4())
        access_token, access_expires = self._jwt_service.create_access_token(user_id=user_id,permissions=permissions)
        refresh_token, refresh_expires = self._jwt_service.create_refresh_token(user_id=user_id,token_id=token_id)
        return AuthResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires=access_expires,
            refresh_token_expires=refresh_expires,
            user_id=user_id,
            username=username,
            email=email,
            permissions=permissions
        )