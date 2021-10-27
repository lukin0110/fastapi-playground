"""Users."""
import traceback
from typing import List

from fastapi import APIRouter
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from . import repository
from .mappers import Mapper
from .models import UserCreate, UserModel, UserPatch, UserView

router = APIRouter()


class UserMapper(Mapper[UserModel, UserView, UserCreate, UserPatch]):
    """."""

    last_name = "surname"


@router.get("/", summary="List all users", response_model=List[UserView])
def index() -> List[UserView]:
    return [UserMapper.to_view(user) for user in repository.query()]


@router.post("/", summary="Create a user", response_model=UserView)
def create_user(create: UserCreate) -> UserView:
    model = repository.create(**UserMapper.to_dict(create))
    return UserMapper.to_view(model)


@router.patch("/{user_id}/", summary="Update a user", response_model=UserView)
def patch_user(user_id: int, patch: UserPatch) -> UserView:
    try:
        model = repository.patch(user_id, **UserMapper.to_dict(patch))
        return UserMapper.to_view(model)
    except KeyError:
        traceback.print_exc()
        raise HTTPException(HTTP_404_NOT_FOUND)


@router.get("/full/", summary="List full users", response_model=List[UserModel])
def full() -> List[UserModel]:
    return repository.query()
