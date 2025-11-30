from typing import Annotated

from fastapi import APIRouter, Query, Path, status

from src.database import Message
from src.access_control.dependencies import BusinessElement, PermissionAction, Permit

from .schemas import AccessRule, AccessRuleCreate, AccessRuleUpdate, AccessRules
from .service import AccessRuleService

access_rule_router = APIRouter(prefix="/access_rules", tags=["access_rule"])


@access_rule_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.CREATE)],
    response_model=AccessRule,
)
async def add_access_rule(
    access_rule: AccessRuleCreate,
) -> AccessRule:
    return await AccessRuleService.add_access_rule(access_rule)


@access_rule_router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.CREATE)],
    response_model=list[AccessRule],
)
async def add_access_rules(
    access_rules: list[AccessRuleCreate],
) -> list[AccessRule]:
    return await AccessRuleService.add_access_rules(access_rules)


@access_rule_router.get(
    "/{access_rule_id}",
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.READ_ALL)],
    response_model=AccessRule,
)
async def get_access_rule(access_rule_id: int = Path(...)) -> AccessRule:
    return await AccessRuleService.get_access_rule(access_rule_id)


@access_rule_router.get(
    "",
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.READ_ALL)],
    response_model=AccessRules,
)
async def get_access_rules(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=5)] = 5,
) -> AccessRules:
    data = await AccessRuleService.get_access_rules(offset=offset, limit=limit)
    count = await AccessRuleService.count_access_rules()
    return AccessRules(data=data, count=count)


@access_rule_router.put(
    "/{access_rule_id}",
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.READ_ALL)],
    response_model=AccessRule,
)
async def update_access_rule(
    access_rule: AccessRuleUpdate,
    access_rule_id: int = Path(...),
) -> AccessRule:
    return await AccessRuleService.update_access_rule(access_rule_id, access_rule)


@access_rule_router.delete(
    "/{access_rule_id}",
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.DELETE_ALL)],
    response_model=Message,
)
async def delete_access_rule(
    access_rule_id: int = Path(...),
) -> Message:
    await AccessRuleService.delete_access_rule(access_rule_id)
    return Message(message="AccessRule deleted successfully")
