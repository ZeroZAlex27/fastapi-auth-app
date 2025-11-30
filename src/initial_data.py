import asyncio
import logging

from .exceptions import EntityNotFound
from .config import settings

from .users.service import UserService
from .users.schemas import UserCreate, UserUpdate

from .access_control.access_roles.service import AccessRoleService
from .access_control.business_elements.service import BusinessElementService
from .access_control.access_rules.service import AccessRuleService
from .access_control.access_roles.schemas import AccessRoleCreate
from .access_control.business_elements.schemas import BusinessElementCreate
from .access_control.access_rules.schemas import AccessRuleCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FULL_ACCESS = dict(
    read_permission=True,
    read_all_permission=True,
    create_permission=True,
    update_permission=True,
    update_all_permission=True,
    delete_permission=True,
    delete_all_permission=True,
)

USER_ACCESS = dict(
    read_permission=True,
    read_all_permission=True,
    create_permission=False,
    update_permission=False,
    update_all_permission=False,
    delete_permission=False,
    delete_all_permission=False,
)

AUTH_ACCESS = dict(
    read_permission=True,
    read_all_permission=False,
    create_permission=True,
    update_permission=True,
    update_all_permission=False,
    delete_permission=True,
    delete_all_permission=False,
)


async def init_data():
    logger.info("Checking if superuser exists...")

    try:
        superuser = await UserService.get_user_by_email(settings.FIRST_SUPERUSER_EMAIL)
    except EntityNotFound:
        superuser = None

    if superuser:
        logger.info("Superuser already exists — nothing to initialize.")
        return

    logger.info("Initializing system data...")

    logger.info("Adding access roles...")
    roles = [
        AccessRoleCreate(name="user"),
        AccessRoleCreate(name="admin"),
        AccessRoleCreate(name="manager"),
        AccessRoleCreate(name="guest"),
    ]
    created_roles = await AccessRoleService.add_access_roles(roles)

    role_map = {r.name: r.id for r in created_roles}
    logger.info(f"Roles created. Admin role id = {role_map['admin']}")

    logger.info("Adding business elements...")
    elements = [
        BusinessElementCreate(name="users"),
        BusinessElementCreate(name="access_control"),
        BusinessElementCreate(name="products"),
        BusinessElementCreate(name="orders"),
    ]
    created_elements = await BusinessElementService.add_business_elements(elements)

    element_map = {el.name: el.id for el in created_elements}
    logger.info("Business elements created:", element_map)

    logger.info("Adding access rules...")

    rules = [
        AccessRuleCreate(
            role_id=role_map["admin"],
            business_element_id=element_map["users"],
            **FULL_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["admin"],
            business_element_id=element_map["access_control"],
            **FULL_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["admin"],
            business_element_id=element_map["products"],
            **FULL_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["admin"],
            business_element_id=element_map["orders"],
            **FULL_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["manager"],
            business_element_id=element_map["users"],
            **AUTH_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["user"],
            business_element_id=element_map["users"],
            **AUTH_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["manager"],
            business_element_id=element_map["products"],
            **FULL_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["manager"],
            business_element_id=element_map["orders"],
            **FULL_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["user"],
            business_element_id=element_map["products"],
            **USER_ACCESS,
        ),
        AccessRuleCreate(
            role_id=role_map["user"],
            business_element_id=element_map["orders"],
            **USER_ACCESS,
        ),
    ]

    await AccessRuleService.add_access_rules(rules)
    logger.info("Access rules created.")

    logger.info("Creating superuser...")

    superuser_data = UserCreate(
        email=settings.FIRST_SUPERUSER_EMAIL,
        name="admin",
        surname="admin",
        patronymic="admin",
        password=settings.FIRST_SUPERUSER_PASSWORD,
        password_repeat=settings.FIRST_SUPERUSER_PASSWORD,
    )

    superuser = await UserService.register_new_user(superuser_data)
    logger.info(f"Superuser created: {superuser.email}")

    logger.info("Assigning admin role to superuser...")

    update_data = UserUpdate(access_role_id=role_map["admin"])

    await UserService.update_user_from_superuser(superuser.id, update_data)

    logger.info("Initial data creation completed successfully!")


if __name__ == "__main__":
    asyncio.run(init_data())
