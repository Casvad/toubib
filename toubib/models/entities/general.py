from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel


T = TypeVar("T")

class PageOut(GenericModel, Generic[T]):
    data: List[T]
    total_data: int
    offset: int
    limit: int