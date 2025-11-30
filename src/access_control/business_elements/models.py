from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ...database import Base


class BusinessElementModel(Base):
    __tablename__ = "business_elements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
