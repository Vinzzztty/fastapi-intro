# Must run upload_100_item.py first

from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["tutorial"]
collection_name = "items"


app = FastAPI()


@app.get("/items")
def get_items(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    items = db[collection_name].find().skip(skip).limit(limit)

    items_list = [item for item in items]

    items_list_processed = []

    for item in items_list:
        item["_id"] = str(item["_id"])
        items_list_processed.append(item)

    return items_list_processed


@app.get("/items-sort")
def get_items_sort(sort_by: str = Query(None, description="Field to sort by")):
    sort_order = 1

    if sort_by:
        items = db[collection_name].find().sort(sort_by, sort_order)

    else:
        items = db[collection_name].find()

    items_list = [item for item in items]

    items_list_processed = []

    for item in items_list:
        item["_id"] = str(item["_id"])
        items_list_processed.append(item)

    return items_list_processed
