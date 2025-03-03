from fastapi import APIRouter
from src.pipelines.inference_pipeline import get_recommendations
from src.components.inference_engine import recommend_popular_books
from src.logger import get_logger
from pydantic import BaseModel

custom_logger = get_logger()

class Message(BaseModel):
    query: str
    category:str
    tone:str

router = APIRouter()

# general recommendation
@router.post("/recommendations")
async def gen_recommendation(body: Message):
    try:
        # Get general recommendations
        return get_recommendations(body.query, body.category, body.tone)

    except Exception as e:
        custom_logger.error(f"Error in recommendation endpoint: {e}", exc_info=True )
        return None
    
    
@router.get("/popular_recommendations")
async def pop_recommendation():
    try:
        # Get popular recommendations
        return recommend_popular_books()

    except Exception as e:
        custom_logger.error(f"Error in popular_recommendation endpoint:{e}", exc_info=True)
        return None
    
    

