from .models import BusinessElementModel
from .schemas import BusinessElementCreate, BusinessElementUpdate

from ...dao import BaseDAO


class BusinessElementDAO(
    BaseDAO[BusinessElementModel, BusinessElementCreate, BusinessElementUpdate]
):
    model = BusinessElementModel
