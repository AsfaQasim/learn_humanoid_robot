from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    response_id: str
    feedback: int # 1 for helpful, -1 for not helpful

@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    # This is a placeholder for storing feedback.
    # In a real application, this would store feedback in a database.
    print(f"Received feedback for response {request.response_id}: {request.feedback}")
    return {"message": "Feedback received successfully"}
