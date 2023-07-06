# Python
from typing import Optional
from enum import Enum

# Pydantic 
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path

app = FastAPI()

# Models 
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(example="Guadalajara")
    state: str = Field(example="Jalisco")
    conuntry: str = Field(example="México")

class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="Luis")
    last_name: str = Field(..., min_length=1, max_length=50, example="Garcia")
    age: int = Field(..., gt=0, le=100, example=21)
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):
    password: str = Field(..., min_length=8, example="12345678")

    # UTILIZANDO ESTA SUBCLASE SE PUEDE CREAR LOS EJEMPLOS QUE TENDRÁ LA DOCUMENTACIÓN SWAGGER
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Luis",
    #             "last_name": "Garcia",
    #             "age": 21,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }

class PersonOut(PersonBase):
    pass

@app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {"hello": "world"}

# Request and Response Body

@app.post(path="/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

# Validaciones Query parameter

@app.get(path="/person/detail", status_code=status.HTTP_200_OK)
def show_person(
        name: Optional[str] = Query(None, min_length=1, max_length=50, title="Person Name", description="It's between 1 and 50 characters", example="Luis"), 
        age: str = Query(..., title="Person Age", description="Required", example=25)
    ):
    return {name: age}

# Validaciones Path parameters

@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def show_person(person_id: int = Path(..., gt=0, title="Person Id", description="Person identifier", example=123)):
    return {person_id: "It exists!"}

# Validaciones Request Body 

@app.put(path="/person/{person_id}", status_code=status.HTTP_200_OK)
def update_person(
        person_id: int = Path(..., title="Peson Id", description="This is the person Id", gt=0, example=123),
        person: Person = Body(...),
        location: Location = Body(...)
    ):
    results = person.dict()
    results.update(location.dict())

    return results