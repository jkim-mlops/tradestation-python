from functools import cached_property
from time import time

from pydantic import BaseModel, ConfigDict, computed_field


class TokenInfo(BaseModel):
    model_config = ConfigDict(extra="allow")
    access_token: str
    id_token: str
    scope: str
    expires_in: int

    @computed_field
    @cached_property
    def expires_at(self) -> int:
        return int(time()) + self.expires_in


class TokenInfoWithRefresh(TokenInfo):
    refresh_token: str
