from pydantic import BaseModel, UUID4, JsonValue

class OutputSchema(BaseModel):
    
    id: UUID4
    #location

def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    return type(obj).__class__.__name__ == "ModelMetaclass"

def parse_schema(schema):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = dict(schema)
    
    for key, value in parsed_schema.items():
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                child_parsed_schema = []
                for item in value:
                    child_dict = parse_schema(item)
                    child_parsed_schema.append(item.Meta.orm_model(**child_dict))
                parsed_schema[key] = child_parsed_schema
            elif is_pydantic(value):
                child_dict = parse_schema(value)
                parsed_schema[key] = value.Meta.orm_model(
                    **child_dict
                )
        except AttributeError:
            raise AttributeError(
                f"Found nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified."
            )
    return parsed_schema

class PlotlyJSONSchema(BaseModel):
    data: JsonValue
    layout: JsonValue