from pydantic import BaseModel, Field


class AccessRuleUpdate(BaseModel):
    read_permission: bool = Field(False)
    read_all_permission: bool = Field(False)

    create_permission: bool = Field(False)

    update_permission: bool = Field(False)
    update_all_permission: bool = Field(False)

    delete_permission: bool = Field(False)
    delete_all_permission: bool = Field(False)

    role_id: int | None = Field(default=None)
    business_element_id: int | None = Field(default=None)


class AccessRuleCreate(AccessRuleUpdate):
    role_id: int
    business_element_id: int


class AccessRule(AccessRuleCreate):
    id: int

    class Config:
        from_attributes = True


class AccessRules(BaseModel):
    data: list[AccessRule]
    count: int
