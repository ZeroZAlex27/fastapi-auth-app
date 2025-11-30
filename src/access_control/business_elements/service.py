from src.exceptions import EntityAlreadyExists, EntityNotFound

from ...database import async_session_maker
from .schemas import BusinessElementCreate, BusinessElementUpdate
from .models import BusinessElementModel
from .dao import BusinessElementDAO


class BusinessElementService:
    @classmethod
    async def add_business_element(
        cls, business_element: BusinessElementCreate
    ) -> BusinessElementModel:
        async with async_session_maker() as session:
            business_element_exist = await BusinessElementDAO.find_one_or_none(
                session, name=business_element.name
            )
            if business_element_exist:
                raise EntityAlreadyExists("business_element")

            db_business_element = await BusinessElementDAO.add(
                session, business_element
            )
            await session.commit()
        return db_business_element

    @classmethod
    async def add_business_elements(
        cls, business_elements: list[BusinessElementCreate]
    ) -> list[BusinessElementModel]:
        async with async_session_maker() as session:
            db_business_elements = await BusinessElementDAO.add_bulk(
                session, business_elements
            )
            await session.commit()
        return db_business_elements

    @classmethod
    async def get_business_element(
        cls, business_element_id: int
    ) -> BusinessElementModel:
        async with async_session_maker() as session:
            db_business_element = await BusinessElementDAO.find_one_or_none(
                session, id=business_element_id
            )
        if db_business_element is None:
            raise EntityNotFound("business_element")
        return db_business_element

    @classmethod
    async def get_business_element_by_name(
        cls, business_element_name: str
    ) -> BusinessElementModel:
        async with async_session_maker() as session:
            db_business_element = await BusinessElementDAO.find_one_or_none(
                session, name=business_element_name
            )
        if db_business_element is None:
            raise EntityNotFound("business_element")
        return db_business_element

    @classmethod
    async def get_business_elements(
        cls,
        *filter,
        offset: int = 0,
        limit: int = 5,
        **filter_by,
    ) -> list[BusinessElementModel]:
        async with async_session_maker() as session:
            business_elements = await BusinessElementDAO.find_all(
                session, offset=offset, limit=limit, *filter, **filter_by
            )
        if not business_elements:
            raise EntityNotFound("business_element")
        return business_elements

    @classmethod
    async def update_business_element(
        cls, business_element_id: int, business_element: BusinessElementUpdate
    ) -> BusinessElementModel:
        async with async_session_maker() as session:
            db_business_element = await BusinessElementDAO.find_one_or_none(
                session, BusinessElementModel.id == business_element_id
            )
            if db_business_element is None:
                raise EntityNotFound("business_element")

            business_element_in = business_element.model_dump(exclude_unset=True)
            business_element_update = await BusinessElementDAO.update(
                session,
                BusinessElementModel.id == business_element_id,
                object_in=business_element_in,
            )
            await session.commit()
        return business_element_update

    @classmethod
    async def delete_business_element(cls, business_element_id: int) -> None:
        async with async_session_maker() as session:
            await BusinessElementDAO.delete(
                session, BusinessElementModel.id == business_element_id
            )
            await session.commit()

    @classmethod
    async def count_business_elements(cls, *filter, **filter_by) -> int:
        async with async_session_maker() as session:
            count = await BusinessElementDAO.count(session, *filter, **filter_by)
        return count or 0
