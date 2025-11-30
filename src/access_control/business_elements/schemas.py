from pydantic import BaseModel, Field


class BusinessElementUpdate(BaseModel):
    name: str | None = Field(default=None)


class BusinessElementCreate(BusinessElementUpdate):
    name: str


class BusinessElement(BusinessElementCreate):
    id: int

    class Config:
        from_attributes = True


class BusinessElements(BaseModel):
    data: list[BusinessElement]
    count: int
