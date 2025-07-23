from fastapi import APIRouter
from app.models import ScoreSubmission
from app.crud import submit_score, get_top_players, get_user_rank

router = APIRouter()

@router.post("/submit")
async def submit_score_api(payload: ScoreSubmission):
    await submit_score(payload.user_id, payload.score)
    return {"message": "Score submitted"}

@router.get("/top")
async def get_top_api():
    top = await get_top_players()
    return top

@router.get("/rank/{user_id}")
async def get_rank_api(user_id: str):
    return await get_user_rank(user_id)
