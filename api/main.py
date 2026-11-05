from fastapi import FastAPI

app = FastAPI(
    title="GeotecData API",
    description="API para análisis geológico y geotécnico",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Bienvenido a GeotecData API",
        "status": "online"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}