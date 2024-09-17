from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()


async def custom_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


app.add_exception_handler(Exception, custom_exception_handler)


@app.get("/custom")
async def custom_endpoint():
    try:
        result = 1 / 0

        return {"result": result}

    except Exception as e:
        return await custom_exception_handler(None, e)
