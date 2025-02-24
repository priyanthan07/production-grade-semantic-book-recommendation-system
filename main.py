import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="book-recommendation-system",
    description="This API provides chat functionalities for the recommendation system.",
    version="1.0.0",
    swagger_ui_parameters={"displayRequestDuration": True},
)

app.include_router()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to log requests for troubleshooting
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Basic route to confirm server is running
@app.get("/")
async def root():
    return {"message": "FastAPI server is running"}

# Health check route (useful for debugging and testing)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port= 8000, reload=True)