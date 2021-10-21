"""Users."""
from typing import Annotated, Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

router = APIRouter()

ID = Annotated[
    int, Field(title="User ID", description="Unique ID of the user.", example="1")
]
FirstName = Annotated[str, Field(title="First name", example="Jeff")]
LastName = Annotated[Optional[str], Field(title="Last name", example="Lebowski")]
Email = Annotated[
    EmailStr,
    Field(
        default_factory=lambda: "jeff@dudeism.com",
        title="Email of the user",
        example="dude@dudeism.com",
    ),
]


#######################################################
# Database Models
#######################################################
class UserModel(BaseModel):
    """Full user object"""

    id: ID
    first_name: FirstName
    last_name: LastName
    email: Email


#######################################################
# API Models
#######################################################
class UserPatch(BaseModel):
    """Create a user."""

    first_name: FirstName
    surname: LastName
    email: Email


class UserView(BaseModel):
    """Customized view on a UserModel."""

    id: ID
    first_name: FirstName
    surname: LastName


users_db: Dict[int, UserModel] = {
    1: UserModel(
        id=1,
        first_name="Donny",
        last_name="Kerabatsos",
        email=EmailStr("donny@dudeism.com"),
    )
}


class Mapper:
    # Maps model fields to views
    map: Dict[str, str] = {"last_name": "surname"}

    @classmethod
    def to_view(cls, model: UserModel) -> UserView:
        """Transform a UserModel to a UserView."""
        data = model.dict()
        for model_field, view_field in cls.map.items():
            data[view_field] = data.pop(model_field)
        return UserView.parse_obj(data)

    @classmethod
    def to_model(cls, patch: UserPatch, **kwargs: Any) -> UserModel:
        """Transform a UserCreate to a UserModel."""
        data = {**kwargs, **patch.dict()}
        for model_field, view_field in cls.map.items():
            data[model_field] = data.pop(view_field)
        return UserModel.parse_obj(data)

    @classmethod
    def to_dict(cls, patch: UserPatch) -> Dict[str, Any]:
        data = patch.dict(exclude_unset=True)
        for model_field, view_field in cls.map.items():
            data[model_field] = data.pop(view_field)
        return data


@router.get("/", response_model=List[UserView])
def index() -> List[UserView]:
    return [Mapper.to_view(user) for user in users_db.values()]


@router.post("/", response_model=UserView)
def create_user(patch: UserPatch) -> UserView:
    user_id = max(users_db.keys() or {0}) + 1
    users_db[user_id] = Mapper.to_model(patch, id=user_id)
    return Mapper.to_view(users_db[user_id])


@router.patch("/{user_id}/", response_model=UserView)
def patch_user(user_id: int, patch: UserPatch) -> UserView:
    try:
        model = users_db[user_id]
        data = {**model.dict(), **Mapper.to_dict(patch)}
        updated = UserModel.parse_obj(data)
        users_db[user_id] = updated
        return Mapper.to_view(updated)
    except KeyError:
        raise HTTPException(HTTP_404_NOT_FOUND)


@router.get("/full/", response_model=List[UserModel])
def full() -> List[UserModel]:
    return [user for user in users_db.values()]
