from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color
from typing import List, Optional

class SectionModel(BaseModel):
    name:str = Field(...)
    top: float = Field(...)
    bottom: float = Field(...)

    class Config:
        validate_assignment = True
        
class OpenHole(SectionModel):
    diameter: float = Field(...)  
    color: Color = Field('#cfd4d3')
    hatch: Optional[str] = Field(None)



    
class Cement(SectionModel):
    oh: float = Field(...) 
    color: Color = Field('#60b1eb')
    hatch: str = Field('.')


    
class Perforation(SectionModel):
    oh: float = Field(...) 
    color: Color = Field('#030302')
    hatch: str = Field('*')
    scale: float = Field(1)
    penetrate: float = Field(1.1)


    
class Casing(SectionModel):
    diameter: float = Field(...) 
    cement: List[Optional[Cement]] = Field(None)
    perforations: List[Optional[Perforation]]  = Field(None)
    pipe_width: float = Field(0.03, gt=0)
    shoe_scale: float = Field(5, gt=0)
    color: Color = Field('Black')
    

        
class Tubing(SectionModel):
    diameter: float  = Field(...)
    pipe_width: float = Field(0.02, gt=0)
    color: Color = Field('#828783')
    hatch: str = Field(None)


    
class BridgePlug(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#7a2222')
    hatch: str = Field('xx')



class Sleeve(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#74876d')
    hatch: str = Field('|')


    
class Plug(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#60b1eb')
    hatch: str = Field('..')



class Packer(SectionModel):
    diameter: float  = Field(...)
    inner_diameter: float  = Field(...)
    color: Color = Field('#7a2222')
    hatch: str = Field('xx')


    

    

    
    

