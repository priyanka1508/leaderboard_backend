from pydantic import BaseModel

class ScoreSubmission(BaseModel):
    user_id: str
    score: int

class LeaderboardEntry(BaseModel):
    user_id: str
    total_score: int
    rank: int
