from fastapi import FastAPI

app = FastAPI()
app.title="First app whit FastApi"
app.version = "0.0.1"

@app.get("/", tags= ["Home"])
def read_root():
    return "hello world get" 