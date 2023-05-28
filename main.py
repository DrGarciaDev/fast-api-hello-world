# Python
from typing import Optional
from enum import Enum

# Pydantic 
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import FastAPI
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
    city: str
    state: str
    conuntry: str

class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=100)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


@app.get("/")
def home():
    return {"hello": "world"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones Query parameter

@app.get("/person/detail")
def show_person(
        name: Optional[str] = Query(None, min_length=1, max_length=50, title="Person Name", description="It's between 1 and 50 characters"), 
        age: str = Query(..., title="Person Age", description="Required")
    ):
    return {name: age}

# Validaciones Path parameters

@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(..., gt=0, title="Person Id", description="Person identifier")):
    return {person_id: "It exists!"}

# Validaciones Request Body 

@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(..., title="Peson Id", description="This is the person Id", gt=0),
        person: Person = Body(...),
        location: Location = Body(...)
    ):
    results = person.dict()
    results.update(location.dict())

    return results