"""."""
from typing import Dict, List

from pydantic import EmailStr

from .models import UserModel

_users_db: Dict[int, UserModel] = {
    1: UserModel(
        id=1,
        first_name="Donny",
        last_name="Kerabatsos",
        email=EmailStr("donny@dudeism.com"),
    )
}


def query() -> List[UserModel]:
    """Query the repository."""
    return list(_users_db.values())


def create(**kwargs) -> UserModel:
    """Create a user."""
    user_id = max(_users_db.keys() or {0}) + 1
    kwargs["id"] = user_id
    model: UserModel = UserModel.parse_obj(kwargs)
    _users_db[user_id] = model
    return model


def patch(user_id: int, **kwargs) -> UserModel:
    """Patch a user."""
    model = _users_db[user_id]
    data = {**model.dict(), **kwargs}
    updated = UserModel.parse_obj(data)
    _users_db[user_id] = updated
    return updated
