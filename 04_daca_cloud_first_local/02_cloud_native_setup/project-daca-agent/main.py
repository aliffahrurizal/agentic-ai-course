from fastapi import FastAPI

app = FastAPI(
    title="DACA Agent",
    description="DACA Agent is a FastAPI application that provides a REST API for the DACA Agent.",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": f"Hello from DACA Agent - Super!"}
