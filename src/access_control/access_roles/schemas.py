from pydantic import BaseModel, Field


class AccessRoleUpdate(BaseModel):
    name: str | None = Field(default=None)


class AccessRoleCreate(AccessRoleUpdate):
    name: str


class AccessRole(AccessRoleCreate):
    id: int

    class Config:
        from_attributes = True


class AccessRoles(BaseModel):
    data: list[AccessRole]
    count: int
