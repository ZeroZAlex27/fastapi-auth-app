from typing import Annotated

from fastapi import APIRouter, Query, Path, status

from ...database import Message
from ..dependencies import BusinessElement, PermissionAction, Permit

from .models import AccessRoleModel
from .schemas import AccessRole, AccessRoleCreate, AccessRoleUpdate, AccessRoles
from .service import AccessRoleService

access_role_router = APIRouter(prefix="/access_roles", tags=["access_role"])


@access_role_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.CREATE)],
    response_model=AccessRole,
)
async def add_access_role(
    access_role: AccessRoleCreate,
) -> AccessRole:
    return await AccessRoleService.add_access_role(access_role)


@access_role_router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.CREATE)],
    response_model=list[AccessRole],
)
async def add_access_roles(
    access_roles: list[AccessRoleCreate],
) -> list[AccessRole]:
    return await AccessRoleService.add_access_roles(access_roles)


@access_role_router.get(
    "/{access_role_id}",
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.READ_ALL)],
    response_model=AccessRole,
)
async def get_access_role(access_role_id: int = Path(...)) -> AccessRole:
    return await AccessRoleService.get_access_role(access_role_id)


@access_role_router.get(
    "",
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.READ_ALL)],
    response_model=AccessRoles,
)
async def get_access_roles(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=5)] = 5,
    name: Annotated[str | None, Query(max_length=50)] = None,
) -> AccessRoles:
    filter = []

    if name:
        filter.append(AccessRoleModel.name.ilike(f"%{name}%"))

    data = await AccessRoleService.get_access_roles(*filter, offset=offset, limit=limit)
    count = await AccessRoleService.count_access_roles(*filter)
    return AccessRoles(data=data, count=count)


@access_role_router.put(
    "/{access_role_id}",
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.UPDATE_ALL)],
    response_model=AccessRole,
)
async def update_access_role(
    access_role: AccessRoleUpdate,
    access_role_id: int = Path(...),
) -> AccessRole:
    return await AccessRoleService.update_access_role(access_role_id, access_role)


@access_role_router.delete(
    "/{access_role_id}",
    dependencies=[Permit(BusinessElement.ACCESS_CONTROL, PermissionAction.DELETE_ALL)],
    response_model=Message,
)
async def delete_access_role(
    access_role_id: int = Path(...),
) -> Message:
    await AccessRoleService.delete_access_role(access_role_id)
    return Message(message="AccessRole deleted successfully")
