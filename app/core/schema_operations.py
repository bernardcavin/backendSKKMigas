from anyio import value
from click import Option
from pydantic import BaseModel, JsonValue
from typing import Any, Optional, get_args
from pydantic._internal._model_construction import ModelMetaclass

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None

from fastapi import HTTPException

def create_api_response(success: bool, message: str, data: dict = None, status_code: int = 200):
    if not success:
        raise HTTPException(status_code=status_code, detail=message)
    
    output = {
        "success": success,
        "message": message,
    }
    
    if data:
        output["data"] = data
    
    return output

class PlotlyJSONSchema(BaseModel):
    data: JsonValue
    layout: JsonValue

def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    return type(obj).__class__.__name__ == "ModelMetaclass"

def model_from_dict(model, data: dict):
    """
    Updates the attributes of an SQLAlchemy model instance from a dictionary,
    ignoring keys that are not present in the data or are set to None.
    """
    new_data = {}
    for key, value in data.items():
        if value is not None and hasattr(model, key):
            new_data[key] = value
    return model(**new_data)

def parse_schema(schema):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    
    parsed_schema = dict(schema)
    
    parsed_schema_copy = parsed_schema.copy()
    
    for key, value in parsed_schema_copy.items():
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                child_parsed_schema = []
                for item in value:
                    child_dict = parse_schema(item)
                    child_parsed_schema.append(model_from_dict(item.Meta.orm_model, child_dict))
                parsed_schema[key] = child_parsed_schema
            elif is_pydantic(value):
                child_dict = parse_schema(value)
                parsed_schema[key] = model_from_dict(
                    value.Meta.orm_model,
                    child_dict
                )
            elif value is None:
                del parsed_schema[key]
        except AttributeError:
            raise AttributeError(
                f"Found nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified."
            )
    return parsed_schema
        
            

# class AllRequired(ModelMetaclass):
#     def __new__(self, name, bases, namespaces, **kwargs):
#         annotations = namespaces.get('__annotations__', {})
#         print(annotations)
#         for base in bases:
#             annotations.update(base.__annotations__)
#         for field in annotations:
#             if not field.startswith('__'):
#                 if getattr(annotations[field], '_name', None) is "Optional":
#                     annotations[field] = get_args(annotations[field])[0]
#                 else:
#                     annotations[field] = annotations[field]
#         namespaces['__annotations__'] = annotations
#         return super().__new__(self, name, bases, namespaces, **kwargs)