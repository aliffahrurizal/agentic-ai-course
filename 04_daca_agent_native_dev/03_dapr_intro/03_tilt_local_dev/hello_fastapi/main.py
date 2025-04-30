from fastapi import FastAPI

app = FastAPI(title="Dapr FastAPI Hello World")

@app.get("/")
async def root():
    return {"message": "Hello from Live AGI!"}

@app.get("/name")
async def root_user():
    return {"user": "admin!"}


# cloud native agents
# problems in cloud
# wWhy daca is good for agent native cloud?
# 