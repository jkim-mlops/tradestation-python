from pydantic import BaseModel, ConfigDict


class OpenID(BaseModel):
    model_config = ConfigDict(extra="allow")
    authorization_endpoint: str
    token_endpoint: str
