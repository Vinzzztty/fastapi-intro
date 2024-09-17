import logging
from fastapi import FastAPI

app = FastAPI(debug=False)

logging.basicConfig(level=logging.INFO)


@app.get("/greet/")
def greet(name: str):
    logging.info(f"Greeting request received for {name}")
    return {"message": f"Hello, {name}"}
