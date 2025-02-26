from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class Message(BaseModel):
    pool: str
    sessionId: str
    messages: list[dict]
    modelConfig: dict


router = APIRouter()


# Invoke the transcripts to SQS Queue
@router.post("/recommendation")
async def keyserver_call(body: Message):
    try:
        pass

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing: {e}")
