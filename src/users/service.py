from uuid import UUID

from src.exceptions import EntityAlreadyExists, EntityNotFound

from ..database import async_session_maker
from ..auth.utils import get_password_hash
from .schemas import (
    UserCreate,
    UserUpdate,
    UserCreateDB,
    UserUpdateDB,
)
from .models import UserModel
from .dao import UserDAO


class UserService:
    @classmethod
    async def register_new_user(cls, user: UserCreate) -> UserModel:
        async with async_session_maker() as session:
            user_exist = await UserDAO.find_one_or_none(session, email=user.email)
            if user_exist:
                raise EntityAlreadyExists("user")

            db_user = await UserDAO.add(
                session,
                UserCreateDB(
                    **user.model_dump(
                        exclude={"password", "password_repeat"},
                    ),
                    hashed_password=get_password_hash(user.password)
                ),
            )
            await session.commit()
        return db_user

    @classmethod
    async def get_user(cls, user_id: UUID) -> UserModel:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, id=user_id)
        if db_user is None:
            raise EntityNotFound("user")
        return db_user

    @classmethod
    async def get_user_by_email(cls, email: str) -> UserModel:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, email=email)
        if db_user is None:
            raise EntityNotFound("user")
        return db_user

    @classmethod
    async def update_user(cls, user_id: UUID, user: UserUpdate) -> UserModel:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, UserModel.id == user_id)
            if db_user is None:
                raise EntityNotFound("user")

            if user.password:
                user_in = UserUpdateDB(
                    **user.model_dump(
                        exclude={
                            "is_active",
                            "access_role_id",
                            "password",
                            "password_repeat",
                        },
                        exclude_unset=True,
                    ),
                    hashed_password=get_password_hash(user.password)
                )
            else:
                user_in = user.model_dump(exclude_unset=True)

            user_update = await UserDAO.update(
                session, UserModel.id == user_id, object_in=user_in
            )
            await session.commit()
            return user_update

    @classmethod
    async def delete_user(cls, user_id: UUID) -> None:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, id=user_id)
            if db_user is None:
                raise EntityNotFound("user")
            await UserDAO.update(
                session, UserModel.id == user_id, object_in={"is_active": False}
            )
            await session.commit()

    @classmethod
    async def get_users_list(
        cls, *filter, offset: int = 0, limit: int = 100, **filter_by
    ) -> list[UserModel]:
        async with async_session_maker() as session:
            users = await UserDAO.find_all(
                session, *filter, offset=offset, limit=limit, **filter_by
            )
        if not users:
            raise EntityNotFound("user")
        return users

    @classmethod
    async def update_user_from_superuser(
        cls, user_id: UUID, user: UserUpdate
    ) -> UserModel:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, UserModel.id == user_id)
            if db_user is None:
                raise EntityNotFound("user")

            user_in = user.model_dump(exclude_unset=True)
            user_update = await UserDAO.update(
                session, UserModel.id == user_id, object_in=user_in
            )
            await session.commit()
            return user_update

    @classmethod
    async def delete_user_from_superuser(cls, user_id: UUID) -> None:
        async with async_session_maker() as session:
            await UserDAO.delete(session, UserModel.id == user_id)
            await session.commit()
