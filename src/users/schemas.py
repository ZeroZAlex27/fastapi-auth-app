from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserBase(BaseModel):
    email: EmailStr | None = Field(None)
    name: str | None = Field(None)
    surname: str | None = Field(None)
    patronymic: str | None = Field(None)
    is_active: bool = Field(True)
    access_role_id: int | None = Field(default=None)


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    patronymic: str
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self


class UserUpdate(UserBase):
    password: str | None = None
    password_repeat: str | None = None

    @model_validator(mode="after")
    def validate_password_change(self):
        if (
            self.password or self.password_repeat
        ) and self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self


class User(UserBase):
    id: UUID
    email: EmailStr
    name: str
    surname: str
    patronymic: str
    is_active: bool
    access_role_id: int

    class Config:
        from_attributes = True


class UserCreateDB(UserBase):
    hashed_password: str | None = None


class UserUpdateDB(UserBase):
    hashed_password: str
