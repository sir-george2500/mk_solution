from fastapi import FastAPI

app = FastAPI(title="MK Solution", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to My FastAPI App"}

