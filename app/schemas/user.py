from pydantic import BaseModel, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    username: str 
    email: EmailStr = Field(
        ...,
        description="user email, by this field the user would log in the app",
        example="milagrosalvarez2604@gmail.com"
    )
    password: str = Field(
        ...,
        description="user password, also used to log in the app",
        min_length=6,
        example="Password1"
    )

    @field_validator("password")
    @classmethod
    def password_must_contain_number(cls, value: str):
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        return value

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminUserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True