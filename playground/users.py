"""Users."""
from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()


class UserFields:
    """Field definitions."""

    ID = Field(
        ...,
        title="User ID",
    )
    FIRST_NAME = Field(..., title="First name", example="Jeff")
    LAST_NAME = Field(..., title="Last name", example="Lebowski")
    EMAIL = Field(..., title="Email of the user", example="dude@dudeism.com")


class UserCreate(BaseModel):
    """Create a user."""

    first_name: str = UserFields.FIRST_NAME
    last_name: str = UserFields.LAST_NAME
    email: EmailStr = UserFields.EMAIL


class UserModel(UserCreate):
    """Full user object"""

    id: int = UserFields.ID


class UserView(BaseModel):
    """."""

    id: int = UserFields.ID
    first_name: str = UserFields.FIRST_NAME
    surname: str = UserFields.LAST_NAME


users_db: Dict[int, UserModel] = {
    1: UserModel(
        id=1,
        first_name="Donny",
        last_name="Kerabatsos",
        email=EmailStr("donny@dudeism.com"),
    )
}


def mapper(model: UserModel) -> UserView:
    """Transform a UserModel to a UserView."""
    data = model.dict()
    data["surname"] = data.pop("last_name")
    return UserView.parse_obj(data)


@router.get("/", response_model=List[UserView])
def index() -> List[UserView]:
    return [mapper(user) for user in users_db.values()]


@router.post("/", response_model=UserView)
def create(body: UserCreate) -> UserView:
    new_id = max(users_db.keys() or {0}) + 1
    data = {"id": new_id, **body.dict()}
    users_db[new_id] = UserModel.parse_obj(data)
    return UserView.parse_obj(data)
