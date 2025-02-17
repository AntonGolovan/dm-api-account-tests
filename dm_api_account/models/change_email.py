from pydantic import BaseModel, Field, ConfigDict


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='логин')
    password: str = Field(..., description='пароль')
    email: str = Field(..., description='Email')
