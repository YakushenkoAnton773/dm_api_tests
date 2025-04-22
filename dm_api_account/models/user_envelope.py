from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NanneModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"

class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class User(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None, alias='smallPictureUrl')
    rating: Rating
    online: datetime = Field(None, alias='smallPictureUrl')
    name: str = Field(None, alias='smallPictureUrl')
    location: str = Field(None, alias='smallPictureUrl')
    registration: datetime = Field(None, alias='smallPictureUrl')


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[User] = None
    metadata: Optional[str] = None
