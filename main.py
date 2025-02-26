import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.logger import custom_logger
from routes import router as rec_router
from alembic.config import Config as AlembicConfig
from alembic.command import upgrade as alembic_upgrade
from apscheduler.schedulers.background import BackgroundScheduler
from src.pipelines.periodic_pipeline import periodic_pipeline
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    alembic_ini_path = (Path(__file__).parent / "alembic.ini").as_posix()
    alembic_cfg = AlembicConfig(str(alembic_ini_path), attributes={"configure_logger": False})

    custom_logger.info("Attempting to run Alembic migrations on startup...")
    try:
        alembic_upgrade(alembic_cfg, "head")  # or however you call it
    except Exception as e:
        custom_logger.error(f"Alembic migrations failed: {e}")
        raise
    else:
        custom_logger.info("Alembic migrations successfully applied.")
        
    custom_logger.info("Alembic migrations completed. Continuing with app startup.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize and start the background scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_pipeline, 'interval', hours=1)
    scheduler.start()
    app.state.scheduler = scheduler
    custom_logger.info("Background scheduler started.")
    
    # Yield control back to the application
    yield

    # Shutdown: gracefully shutdown the scheduler
    if hasattr(app.state, "scheduler"):
        app.state.scheduler.shutdown()
    custom_logger.info("Background scheduler shut down.")

app = FastAPI(
    title="book-recommendation-system",
    description="This API provides chat functionalities for the recommendation system.",
    version="1.0.0",
    swagger_ui_parameters={"displayRequestDuration": True},
    lifespan=lifespan  # Use the lifespan event handler
)

# Include your API routers here if needed
app.include_router(rec_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to log incoming requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    custom_logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    custom_logger.info(f"Response status: {response.status_code}")
    return response

# Basic route to confirm server is running
@app.get("/")
async def root():
    return {"message": "FastAPI server is running"}

# Health check route
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
