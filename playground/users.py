"""Users."""
import traceback
from typing import Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from typing_extensions import Annotated

from .mappers import Mapper

router = APIRouter()


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


users_db: Dict[int, UserModel] = {
    1: UserModel(
        id=1,
        first_name="Donny",
        last_name="Kerabatsos",
        email=EmailStr("donny@dudeism.com"),
    )
}


class UserMapper(Mapper[UserModel, UserView, UserCreate, UserPatch]):
    """."""

    last_name = "surname"


@router.get("/", summary="List all users", response_model=List[UserView])
def index() -> List[UserView]:
    return [UserMapper.to_view(user) for user in users_db.values()]


@router.post("/", summary="Create a user", response_model=UserView)
def create_user(create: UserCreate) -> UserView:
    user_id = max(users_db.keys() or {0}) + 1
    users_db[user_id] = UserMapper.to_model(create, id=user_id)
    return UserMapper.to_view(users_db[user_id])


@router.patch("/{user_id}/", summary="Update a user", response_model=UserView)
def patch_user(user_id: int, patch: UserPatch) -> UserView:
    try:
        model = users_db[user_id]
        data = {**model.dict(), **UserMapper.to_dict(patch)}
        updated = UserModel.parse_obj(data)
        users_db[user_id] = updated
        return UserMapper.to_view(updated)
    except KeyError:
        traceback.print_exc()
        raise HTTPException(HTTP_404_NOT_FOUND)


@router.get("/full/", summary="List full users", response_model=List[UserModel])
def full() -> List[UserModel]:
    return [user for user in users_db.values()]
