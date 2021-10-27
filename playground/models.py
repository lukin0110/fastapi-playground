"""User models."""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated


class UserFields:
    """Annotated field definitions.

    Type definition + metadata.

    https://docs.python.org/3/library/typing.html#typing.Annotated
    """

    _ID = Field(title="User ID", description="Unique ID of the user.", example="1")
    _FirstName = Field(title="First name", example="Jeff")
    _LastName = Field(title="Last name", example="Lebowski")
    _Twitch = Field(title="Twitch Account")
    _Email = Field(
        default_factory=lambda: "jeff@dudeism.com",
        title="Email of the user",
        example="dude@dudeism.com",
    )

    ID = Annotated[int, _ID]
    FirstName = Annotated[str, _FirstName]
    OptionalFirstName = Annotated[Optional[str], _FirstName]
    LastName = Annotated[str, _LastName]
    Twitch = Annotated["TwitchAccount", _Twitch]
    OptionalTwitch = Annotated[Optional["TwitchAccount"], _Twitch]
    OptionalLastName = Annotated[Optional[str], _LastName]
    OptionalEmail = Annotated[Optional[EmailStr], _Email]


#######################################################
# Database Models
#######################################################
class TwitchAccount(BaseModel):
    """Dummy account."""

    twitch_id: Optional[str] = Field(default=None, title="Twitch ID", example="TW1234")
    twitch_username: Optional[str] = Field(
        default=None, title="Twitch Username", example="lukin0110"
    )


class UserModel(BaseModel):
    """Full user object"""

    id: UserFields.ID
    first_name: UserFields.FirstName
    last_name: UserFields.LastName
    twitch: UserFields.OptionalTwitch
    email: UserFields.OptionalEmail


#######################################################
# API Models
#######################################################
class UserCreate(BaseModel):
    """Create a user."""

    first_name: UserFields.FirstName
    surname: UserFields.LastName
    twitch: UserFields.OptionalTwitch
    email: UserFields.OptionalEmail


class UserPatch(BaseModel):
    """Patch a user."""

    first_name: UserFields.OptionalFirstName
    surname: UserFields.OptionalLastName
    twitch: UserFields.OptionalTwitch
    email: UserFields.OptionalEmail


class UserView(BaseModel):
    """Customized view on a UserModel."""

    id: UserFields.ID
    first_name: UserFields.FirstName
    surname: UserFields.LastName
    twitch: UserFields.OptionalTwitch
