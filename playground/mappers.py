"""."""
from typing import Any, Dict, Generic, TypeVar, Union, get_args

from pydantic import BaseModel, parse_obj_as

ViewType = TypeVar("ViewType", bound=BaseModel)
CreateType = TypeVar("CreateType", bound=BaseModel)
PatchType = TypeVar("PatchType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=BaseModel)


class MapperMeta(type):
    """."""

    def __new__(cls, name: str, bases: Any, dct: Dict[str, Any]) -> "MapperMeta":
        new_cls = type.__new__(cls, name, bases, dct)
        cls.map_fields = {k: v for k, v in dct.items() if not k.startswith("__")}
        type_args = get_args(dct["__orig_bases__"][0])
        cls.model_type = type_args[0]
        cls.view_type = type_args[1]
        cls.create_type = type_args[2]
        cls.patch_type = type_args[3]
        return new_cls


class Mapper(Generic[ModelType, ViewType, CreateType, PatchType], metaclass=MapperMeta):
    """."""

    @classmethod
    def to_view(cls, model: ModelType) -> ViewType:
        """Transform a UserModel to a UserView."""
        data = model.dict()
        for model_field, view_field in cls.map_fields.items():
            data[view_field] = data.pop(model_field)
        return parse_obj_as(cls.view_type, data)

    @classmethod
    def to_dict(cls, obj: Union[CreateType, PatchType]) -> Dict[str, Any]:
        data: Dict = obj.dict(exclude_unset=True)
        for model_field, view_field in cls.map_fields.items():
            if view_field in data:
                data[model_field] = data.pop(view_field)
        return data
