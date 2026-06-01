from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from typing import Optional

from app.db.session import get_db
from app.core import security
from app.domains.auth.auth import authenticate_user, sign_up_new_user, get_current_active_user
from app.domains.users.db import user_dtos

auth_router = r = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


def _create_token_response(user) -> dict:
    """Helper to generate a JWT token response for a user."""
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    permissions = "admin" if user.is_superuser else "user"
    access_token = security.create_access_token(
        data={"sub": user.email, "permissions": permissions},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
        },
    }


@r.post("/token", tags=["auth"], summary="Login with OAuth2 form (for Swagger UI)")
async def login(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """Login endpoint using OAuth2 password flow (used by Swagger Authorize button)."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _create_token_response(user)


@r.post("/v1/login", tags=["auth"], summary="Login with JSON body")
async def login_json(
    credentials: RegisterRequest, db=Depends(get_db)
):
    """Login endpoint accepting JSON body (for frontend use)."""
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return _create_token_response(user)


@r.post("/v1/register", tags=["auth"], status_code=201, summary="Register a new user")
async def register(
    user_data: RegisterRequest, db=Depends(get_db)
):
    """Register a new user account."""
    from app.domains.users.db.user_repository import get_user_by_email, create_user
    # Check if user already exists
    existing = get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )
    user = create_user(
        db,
        user_dtos.UserCreate(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_active=True,
            is_superuser=False,
        ),
    )
    return _create_token_response(user)


@r.post("/signup", tags=["auth"], summary="Signup with form data (legacy)")
async def signup(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """Legacy signup endpoint using OAuth2 form."""
    user = sign_up_new_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _create_token_response(user)


@r.get("/v1/me", tags=["auth"], summary="Get current user profile")
async def get_me(current_user=Depends(get_current_active_user)):
    """Get the currently authenticated user's profile."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "is_superuser": current_user.is_superuser,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
    }
