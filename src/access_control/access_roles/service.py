from src.exceptions import EntityAlreadyExists, EntityNotFound

from ...database import async_session_maker
from .schemas import AccessRoleCreate, AccessRoleUpdate
from .models import AccessRoleModel
from .dao import AccessRoleDAO


class AccessRoleService:
    @classmethod
    async def add_access_role(cls, access_role: AccessRoleCreate) -> AccessRoleModel:
        async with async_session_maker() as session:
            access_role_exist = await AccessRoleDAO.find_one_or_none(
                session, name=access_role.name
            )
            if access_role_exist:
                raise EntityAlreadyExists("access_role")

            db_access_role = await AccessRoleDAO.add(session, access_role)
            await session.commit()
        return db_access_role

    @classmethod
    async def add_access_roles(
        cls, access_roles: list[AccessRoleCreate]
    ) -> list[AccessRoleModel]:
        async with async_session_maker() as session:
            db_access_roles = await AccessRoleDAO.add_bulk(session, access_roles)
            await session.commit()
        return db_access_roles

    @classmethod
    async def get_access_role(cls, access_role_id: int) -> AccessRoleModel:
        async with async_session_maker() as session:
            db_access_role = await AccessRoleDAO.find_one_or_none(
                session, id=access_role_id
            )
        if db_access_role is None:
            raise EntityNotFound("access_role")
        return db_access_role

    @classmethod
    async def get_access_roles(
        cls,
        *filter,
        offset: int = 0,
        limit: int = 5,
        **filter_by,
    ) -> list[AccessRoleModel]:
        async with async_session_maker() as session:
            access_roles = await AccessRoleDAO.find_all(
                session, offset=offset, limit=limit, *filter, **filter_by
            )
        if not access_roles:
            raise EntityNotFound("access_role")
        return access_roles

    @classmethod
    async def update_access_role(
        cls, access_role_id: int, access_role: AccessRoleUpdate
    ) -> AccessRoleModel:
        async with async_session_maker() as session:
            db_access_role = await AccessRoleDAO.find_one_or_none(
                session, AccessRoleModel.id == access_role_id
            )
            if db_access_role is None:
                raise EntityNotFound("access_role")

            access_role_in = access_role.model_dump(exclude_unset=True)
            access_role_update = await AccessRoleDAO.update(
                session, AccessRoleModel.id == access_role_id, object_in=access_role_in
            )
            await session.commit()
        return access_role_update

    @classmethod
    async def delete_access_role(cls, access_role_id: int) -> None:
        async with async_session_maker() as session:
            await AccessRoleDAO.delete(session, AccessRoleModel.id == access_role_id)
            await session.commit()

    @classmethod
    async def count_access_roles(cls, *filter, **filter_by) -> int:
        async with async_session_maker() as session:
            count = await AccessRoleDAO.count(session, *filter, **filter_by)
        return count or 0
