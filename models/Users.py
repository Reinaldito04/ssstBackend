from pydantic import BaseModel, Field, field_validator


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    typeUser: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    UID : str
    Code : str
    Status : str
    


class UserResponse(UserBase):
    id: int


class UserLogin(BaseModel):
    name: str
    password: str = Field(...)

    @field_validator('password')
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v
