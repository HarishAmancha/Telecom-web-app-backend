from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security import get_password_hash
from app.models import User
from app.schemas.requests import UserCreateRequest, UserUpdatePasswordRequest
from app.schemas.responses import UserResponse

router = APIRouter()


@router.get("/current", response_model=UserResponse)
async def read_current_user(
        current_user: User = Depends(deps.get_current_user),
) -> User:
    """
    Get current user

    :param current_user: Current user object
    :return: Current user object
    """
    return current_user


@router.delete("/current", status_code=204)
async def delete_current_user(
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> None:
    """
    Delete current user

    :param current_user: Current user object
    :param session: Async session
    """
    await session.execute(delete(User).where(User.id == current_user.id))
    await session.commit()


@router.post("/reset-password", response_model=UserResponse)
async def reset_current_user_password(
        user_update_password: UserUpdatePasswordRequest,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user),
) -> User:
    """
    Update current user password

    :param user_update_password: Password update request object
    :param session: Async session
    :param current_user: Current user object
    :return: Updated user object
    """
    current_user.hashed_password = get_password_hash(user_update_password.password)
    session.add(current_user)
    await session.commit()
    return current_user


@router.post("/register", response_model=UserResponse)
async def register_new_user(
        new_user: UserCreateRequest,
        session: AsyncSession = Depends(deps.get_session),
) -> User:
    """
    Create new user

    :param new_user: New user request object
    :param session: Async session
    :return: New user object
    """
    result = await session.execute(select(User).where(User.email == new_user.email))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Cannot use this email address")
    user = User(
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
    )
    session.add(user)
    await session.commit()
    return user
