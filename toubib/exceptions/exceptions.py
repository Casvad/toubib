from typing import Type, Optional


class EntityNotFoundError(Exception):
    def __init__(self, entity_id: str, entity_type: Type):
        self.entity_id = entity_id
        self.entity_type = entity_type
        super().__init__(f"{entity_type.__name__} with id {entity_id} not found")

class DuplicateKeyException(Exception):
    def __init__(self, duplicated_attribute: str, entity_type: Type):
        self.entity_type = entity_type
        super().__init__(f"{entity_type.__name__} duplicate error: {duplicated_attribute}")

class InvalidArgument(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class IllegalStateException(Exception):
    def __init__(self, msg: str, trace: Optional[Exception] = None):
        super().__init__(msg)
        self.trace = trace