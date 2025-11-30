from .models import AccessRuleModel
from .schemas import AccessRuleCreate, AccessRuleUpdate

from ...dao import BaseDAO


class AccessRuleDAO(BaseDAO[AccessRuleModel, AccessRuleCreate, AccessRuleUpdate]):
    model = AccessRuleModel
