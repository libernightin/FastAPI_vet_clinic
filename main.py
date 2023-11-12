from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', summary='Root')
def root():
    return 'Welcome to our vet clinic'


@app.post('/post')
def create_timestamp():
    new_id = len(post_db)
    new_timestamp = int(datetime.now().timestamp())
    post_db.append(Timestamp(id=new_id, timestamp=new_timestamp))
    return {"id": new_id, "timestamp": new_timestamp}


@app.post('/dog', response_model=Dog)
def get_dogs(dog: Dog):
    new_dog = {
        "pk": len(dogs_db)+1,
        "name": dog.name,
        "kind": dog.kind
    }
    dogs_db.append(new_dog)
    return new_dog


@app.get("/dog", response_model=list[Dog])
def read_dogs(kind: DogType = None):
    if kind:
        return [dog for dog in dogs_db if dog["kind"] == kind]
    return dogs_db


@app.get("/dog/{pk}", response_model=Dog)
def read_dog(pk: int):
    dog = next((dog for dog in dogs_db if dog["pk"] == pk), None)
    if dog:
        return dog
    raise HTTPException(status_code=404, detail="Dog not found")


@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int, dog: Dog):
    index = next((index for index, d in enumerate(dogs_db) if d["pk"] == pk), None)
    if index is not None:
        dogs_db[index]["name"] = dog.name
        dogs_db[index]["kind"] = dog.kind
        return dogs_db[index]
    raise HTTPException(status_code=404, detail="Dog not found")
