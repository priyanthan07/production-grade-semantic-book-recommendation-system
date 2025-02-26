from fastapi import APIRouter
from src.pipelines.inference_pipeline import get_recommendations, recommend_popular_books
from src.logger import custom_logger
from pydantic import BaseModel


class Message(BaseModel):
    query: str
    category:str
    tone:str


router = APIRouter()

# general recommendation
@router.post("/recommendation")
async def gen_recommendation(body: Message):
    try:
        # Get general recommendations
        return get_recommendations(body.query, body.category, body.tone)

    except Exception as e:
        custom_logger.error("Error in recommendation endpoint: %s", e)
        return None
    
    
@router.get("/popular_recommendation")
async def pop_recommendation():
    try:
        # Get popular recommendations
        return recommend_popular_books()

    except Exception as e:
        custom_logger.error("Error in popular_recommendation endpoint: %s", e)
        return None
    
    

