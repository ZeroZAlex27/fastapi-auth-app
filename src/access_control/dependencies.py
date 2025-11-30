from enum import StrEnum

from fastapi import Depends, HTTPException, status

from .business_elements.service import BusinessElementService
from .access_rules.service import AccessRuleService
from ..users.models import UserModel

from ..auth.dependencies import get_current_user


class BusinessElement(StrEnum):
    USERS = "users"
    ACCESS_CONTROL = "access_control"
    PRODUCTS = "products"
    ORDERS = "orders"


class PermissionAction(StrEnum):
    READ = "read"
    READ_ALL = "read_all"
    CREATE = "create"
    UPDATE = "update"
    UPDATE_ALL = "update_all"
    DELETE = "delete"
    DELETE_ALL = "delete_all"


def Permit(element: BusinessElement, action: PermissionAction):
    async def inner(user: UserModel = Depends(get_current_user)):
        return await allow(element, action, user)

    return Depends(inner)


async def allow(
    element: BusinessElement,
    action: PermissionAction,
    user: UserModel = Depends(get_current_user),
):
    business_element = await BusinessElementService.get_business_element_by_name(
        element
    )

    if not business_element:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Business element not found",
        )

    if not user.access_role_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No access role assigned"
        )

    access_rule = await AccessRuleService.get_access_rule_for_role_and_element(
        user.access_role_id, business_element.id
    )

    if not access_rule:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access assigned",
        )

    permission_field = f"{action.value}_permission"

    if not getattr(access_rule, permission_field, False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return True
