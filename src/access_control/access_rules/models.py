from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ...database import Base


class AccessRuleModel(Base):
    __tablename__ = "access_roles_rules"

    __table_args__ = (
        UniqueConstraint(
            "role_id", "business_element_id", name="uq_role_business_element"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    read_permission: Mapped[bool] = mapped_column(Boolean, default=False)
    read_all_permission: Mapped[bool] = mapped_column(Boolean, default=False)

    create_permission: Mapped[bool] = mapped_column(Boolean, default=False)

    update_permission: Mapped[bool] = mapped_column(Boolean, default=False)
    update_all_permission: Mapped[bool] = mapped_column(Boolean, default=False)

    delete_permission: Mapped[bool] = mapped_column(Boolean, default=False)
    delete_all_permission: Mapped[bool] = mapped_column(Boolean, default=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("access_roles.id"))
    business_element_id: Mapped[int] = mapped_column(ForeignKey("business_elements.id"))
