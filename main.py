# Python
from typing import Optional
from enum import Enum

# Pydantic 
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

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

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel2021")
    message: str = Field(default="Login Succesfully!")

@app.get(path="/", status_code=status.HTTP_200_OK, tags=["Home"])
def home():
    return {"hello": "world"}

# Request and Response Body

@app.post(path="/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED, tags=["Persons"], summary="Create Person in the app")
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the information in the database

    Parameters:
    - Reqeust body parameters:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status

    Returns a person model with first name, last name, age, hair colo and marital status
    """
    return person

# Validaciones Query parameter

@app.get(path="/person/detail", status_code=status.HTTP_200_OK, tags=["Persons"])
def show_person(
        name: Optional[str] = Query(None, min_length=1, max_length=50, title="Person Name", description="It's between 1 and 50 characters", example="Luis"), 
        age: str = Query(..., title="Person Age", description="Required", example=25)
    ):
    return {name: age}

# Validaciones Path parameters

persons = [1,2,3,4,5]

@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK, tags=["Persons"])
def show_person(person_id: int = Path(..., gt=0, title="Person Id", description="Person identifier", example=123)):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡ This person doesn't exist !"
        )
    return {person_id: "It exists !"}

# Validaciones Request Body 

@app.put(path="/person/{person_id}", status_code=status.HTTP_200_OK, tags=["Persons"])
def update_person(
        person_id: int = Path(..., title="Peson Id", description="This is the person Id", gt=0, example=123),
        person: Person = Body(...),
        location: Location = Body(...)
    ):
    results = person.dict()
    results.update(location.dict())

    return results

# forms 

@app.post(path="/login", response_model=LoginOut, status_code=status.HTTP_200_OK, tags=["Persons"])
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers parameters

@app.post(path="/contact", status_code=status.HTTP_200_OK, tags=["About"])
def contact(
    first_name: str = Form(..., max_length=20, min_length=1), 
    last_name: str = Form(..., max_length=20, min_length=1), 
    email: EmailStr = Form(...),
    message: str = Form(..., min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# files 

@app.post(path="/post-image", tags=["Files"])
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    }