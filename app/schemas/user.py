from pydantic import BaseModel, ConfigDict, Field, model_validator


class UserRegister(BaseModel):
    email: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8)
    repeat_password: str = Field(min_length=8)

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.repeat_password:
            raise ValueError("Passwords do not match")

        return self
    
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"