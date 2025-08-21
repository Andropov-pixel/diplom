from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import (
    create_access_token,
    verify_password,
    validate_email,
    validate_password
)
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import User, UserCreate, Token
from app.core.dependencies import get_current_user

router = APIRouter()


@router.post("/auth/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/register", response_model=User)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    if not validate_email(user_in.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    if not validate_password(user_in.password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters with uppercase, lowercase and numbers"
        )

    existing_user = await get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await create_user(db, user_in)


@router.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user