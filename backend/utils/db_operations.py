from sqlalchemy.inspection import inspect

def model_to_dict(instance, include_relationships=False):
    data = {c.key: getattr(instance, c.key) for c in inspect(instance).mapper.column_attrs}
    
    if include_relationships:
        for name, relation in inspect(instance).mapper.relationships.items():
            related_value = getattr(instance, name)
            if related_value is not None:
                if relation.uselist:  # If it's a list of related objects
                    data[name] = [model_to_dict(child, include_relationships=False) for child in related_value]
                else:  # If it's a single related object
                    data[name] = model_to_dict(related_value, include_relationships=False)
    
    return data