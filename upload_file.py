from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client["tutorial"]
fs = GridFS(db)

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_id = fs.put(file.file, filename=file.filename, content_type=file.content_type)

    return {"Message": "File uploaded successfully", "file_id": str(file_id)}


@app.get("/file/{file_id}")
async def get_file(file_id: str):
    file_id = ObjectId(file_id)

    grid_out = fs.get(file_id)

    if grid_out is None:
        raise HTTPException(status_code=404, detail="file not found")

    response = Response(content=grid_out.read())
    response.headers["Content-Type"] = grid_out.content_type
    response.headers["Content-Disposition"] = f"attachment: filename{grid_out.filename}"

    return response


@app.get("/file_ids/")
async def get_all_file_ids():
    file_ids = []

    for file_info in db.fs.files.find({}, {"_id": 1}):
        file_ids.append(str(file_info["_id"]))

    return {"file_ids": file_ids}
