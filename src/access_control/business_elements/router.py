from typing import Annotated

from fastapi import APIRouter, Query, Path, status

from ...database import Message
from ..dependencies import (
    BusinessElement as AccessElement,
    PermissionAction,
    Permit,
)

from .models import BusinessElementModel
from .schemas import (
    BusinessElement,
    BusinessElementCreate,
    BusinessElementUpdate,
    BusinessElements,
)
from .service import BusinessElementService

business_element_router = APIRouter(
    prefix="/business_elements", tags=["business_element"]
)


@business_element_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Permit(AccessElement.ACCESS_CONTROL, PermissionAction.CREATE)],
    response_model=BusinessElement,
)
async def add_business_element(
    business_element: BusinessElementCreate,
) -> BusinessElement:
    return await BusinessElementService.add_business_element(business_element)


@business_element_router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Permit(AccessElement.ACCESS_CONTROL, PermissionAction.CREATE)],
    response_model=list[BusinessElement],
)
async def add_business_elements(
    business_elements: list[BusinessElementCreate],
) -> list[BusinessElement]:
    return await BusinessElementService.add_business_elements(business_elements)


@business_element_router.get(
    "/{business_element_id}",
    dependencies=[Permit(AccessElement.ACCESS_CONTROL, PermissionAction.READ_ALL)],
    response_model=BusinessElement,
)
async def get_business_element(business_element_id: int = Path(...)) -> BusinessElement:
    return await BusinessElementService.get_business_element(business_element_id)


@business_element_router.get(
    "",
    dependencies=[Permit(AccessElement.ACCESS_CONTROL, PermissionAction.READ_ALL)],
    response_model=BusinessElements,
)
async def get_business_elements(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=5)] = 5,
    name: Annotated[str | None, Query(max_length=50)] = None,
) -> BusinessElements:
    filter = []

    if name:
        filter.append(BusinessElementModel.name.ilike(f"%{name}%"))

    data = await BusinessElementService.get_business_elements(
        *filter, offset=offset, limit=limit
    )
    count = await BusinessElementService.count_business_elements(*filter)
    return BusinessElements(data=data, count=count)


@business_element_router.put(
    "/{business_element_id}",
    dependencies=[Permit(AccessElement.ACCESS_CONTROL, PermissionAction.UPDATE_ALL)],
    response_model=BusinessElement,
)
async def update_business_element(
    business_element: BusinessElementUpdate,
    business_element_id: int = Path(...),
) -> BusinessElement:
    return await BusinessElementService.update_business_element(
        business_element_id, business_element
    )


@business_element_router.delete(
    "/{business_element_id}",
    dependencies=[Permit(AccessElement.ACCESS_CONTROL, PermissionAction.DELETE_ALL)],
    response_model=Message,
)
async def delete_business_element(
    business_element_id: int = Path(...),
) -> Message:
    await BusinessElementService.delete_business_element(business_element_id)
    return Message(message="BusinessElement deleted successfully")
