from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client["tutorial"]
collection = db["todo"]

app = FastAPI()


class TodoModel(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    done: bool = False


@app.post("/todo")
def create_todo(todo: TodoModel):
    todo = dict(todo)
    todo["_id"] = str(ObjectId())
    collection.insert_one(todo)
    return todo


@app.get("/todos")
def get_all_todo():
    todos = list(collection.find())
    for todo in todos:
        todo["_id"] = str(todo["_id"])

    return todos


@app.get("todo/{id}")
def get_todo_by_id(id: str):
    todo = collection.find_one({"_id": id})

    if todo:
        todo["_id"] = str(todo["_id"])
        return todo

    else:
        raise HTTPException(404, "To Do Not Found")


@app.put("/todo/{id}")
def update_todo(id: str, todo: TodoModel):
    todo_data = todo.dict()

    update_todo = collection.find_one_and_update({"_id": id}, {"$set": todo_data})

    if update_todo:
        return update_todo

    else:
        raise HTTPException(404, "To Do Not Found")


@app.delete("/todo/{id}")
def delete_todo(id: str):
    todo = collection.find_one_and_delete({"_id": id})

    if todo:
        return {"message": f"Todo {id} deleted successfully"}

    else:
        raise HTTPException(404, "To Do Not Found")


@app.put("/todo/{id}/done")
def mark_todo_as_done(id: str):
    todo = collection.find_one_and_update({"_id": id}, {"$set": {"done": True}})

    if todo:
        todo["_id"] = str(todo["_id"])
        return todo

    else:
        raise HTTPException(404, "Todo not Found")
