def extend_flag(inherited,_type):
   def wrapper(final):
     joined = {}
     inherited.append(final)
     for i in inherited:
        for j in i:
           joined[j.name] = j.value
     return _type(final.__name__, joined)
   return wrapper