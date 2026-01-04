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
        example="123456"
    )

    @field_validator("password")
    @classmethod
    def password_min_lenght(cls, value:str):
        if value.__len__ < 6:
            raise ValueError("The password should have at least 6 characters")
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
