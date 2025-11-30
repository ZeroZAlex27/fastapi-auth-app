from src.exceptions import EntityAlreadyExists, EntityNotFound

from ...database import async_session_maker
from .schemas import AccessRuleCreate, AccessRuleUpdate
from .models import AccessRuleModel
from .dao import AccessRuleDAO


class AccessRuleService:
    @classmethod
    async def add_access_rule(cls, access_rule: AccessRuleCreate) -> AccessRuleModel:
        async with async_session_maker() as session:
            access_rule_exist = await AccessRuleDAO.find_one_or_none(
                session,
                role_id=access_rule.role_id,
                business_element_id=access_rule.business_element_id,
            )
            if access_rule_exist:
                raise EntityAlreadyExists("access_rule")

            db_access_rule = await AccessRuleDAO.add(session, access_rule)
            await session.commit()
        return db_access_rule

    @classmethod
    async def add_access_rules(
        cls, access_rules: list[AccessRuleCreate]
    ) -> list[AccessRuleModel]:
        async with async_session_maker() as session:
            db_access_rules = await AccessRuleDAO.add_bulk(session, access_rules)
            await session.commit()
        return db_access_rules

    @classmethod
    async def get_access_rule(cls, access_rule_id: int) -> AccessRuleModel:
        async with async_session_maker() as session:
            db_access_rule = await AccessRuleDAO.find_one_or_none(
                session, id=access_rule_id
            )
        if db_access_rule is None:
            raise EntityNotFound("access_rule")
        return db_access_rule

    @classmethod
    async def get_access_rule_for_role_and_element(
        cls, access_role_id: int, business_element_id: int
    ) -> AccessRuleModel:
        async with async_session_maker() as session:
            db_access_rule = await AccessRuleDAO.find_one_or_none(
                session, role_id=access_role_id, business_element_id=business_element_id
            )
        if db_access_rule is None:
            raise EntityNotFound("access_rule")
        return db_access_rule

    @classmethod
    async def get_access_rules(
        cls,
        *filter,
        offset: int = 0,
        limit: int = 5,
        **filter_by,
    ) -> list[AccessRuleModel]:
        async with async_session_maker() as session:
            access_rules = await AccessRuleDAO.find_all(
                session, offset=offset, limit=limit, *filter, **filter_by
            )
        if not access_rules:
            raise EntityNotFound("access_rule")
        return access_rules

    @classmethod
    async def update_access_rule(
        cls, access_rule_id: int, access_rule: AccessRuleUpdate
    ) -> AccessRuleModel:
        async with async_session_maker() as session:
            db_access_rule = await AccessRuleDAO.find_one_or_none(
                session, AccessRuleModel.id == access_rule_id
            )
            if db_access_rule is None:
                raise EntityNotFound("access_rule")

            access_rule_in = access_rule.model_dump(exclude_unset=True)
            access_rule_update = await AccessRuleDAO.update(
                session, AccessRuleModel.id == access_rule_id, object_in=access_rule_in
            )
            await session.commit()
        return access_rule_update

    @classmethod
    async def delete_access_rule(cls, access_rule_id: int) -> None:
        async with async_session_maker() as session:
            await AccessRuleDAO.delete(session, AccessRuleModel.id == access_rule_id)
            await session.commit()

    @classmethod
    async def count_access_rules(cls, *filter, **filter_by) -> int:
        async with async_session_maker() as session:
            count = await AccessRuleDAO.count(session, *filter, **filter_by)
        return count or 0
