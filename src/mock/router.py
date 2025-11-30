from fastapi import APIRouter, status

from ..database import Message
from ..access_control.dependencies import BusinessElement, PermissionAction, Permit

mock_router = APIRouter(prefix="/mock", tags=["mock"])


@mock_router.get(
    "/products",
    dependencies=[Permit(BusinessElement.PRODUCTS, PermissionAction.READ_ALL)],
)
async def get_products():
    return ["product_1", "product_2"]


@mock_router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Permit(BusinessElement.PRODUCTS, PermissionAction.CREATE)],
)
async def create_product():
    return Message(message="Product created successfully")


@mock_router.get(
    "/orders", dependencies=[Permit(BusinessElement.ORDERS, PermissionAction.READ)]
)
async def get_order():
    return "product_1"


@mock_router.delete(
    "/orders", dependencies=[Permit(BusinessElement.ORDERS, PermissionAction.DELETE)]
)
async def delete_order():
    return Message(message="Order deleted successfully")
