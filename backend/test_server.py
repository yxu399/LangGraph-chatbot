from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "Test server running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_server:app", host="0.0.0.0", port=8000, reload=True)