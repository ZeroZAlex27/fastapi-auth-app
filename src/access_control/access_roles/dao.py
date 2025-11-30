from .models import AccessRoleModel
from .schemas import AccessRoleCreate, AccessRoleUpdate

from ...dao import BaseDAO


class AccessRoleDAO(BaseDAO[AccessRoleModel, AccessRoleCreate, AccessRoleUpdate]):
    model = AccessRoleModel
