from app.db import db
from bson import ObjectId
from dotenv import load_dotenv
import os

# load_dotenv()
# BACKEND_DOMAIN = os.getenv("BACKEND_DOMAIN")

async def submit_score(user_id: str, score: int):
    user_id = int(user_id)
    
    # Insert new game session
    await db.game_sessions.insert_one({
        "user_id": user_id,
        "score": score
    })

    # Atomically update leaderboard
    await db.leaderboard.update_one(
        {"user_id": user_id},
        {"$inc": {"total_score": score}},
        upsert=True
    )

    # Fire off rank calculation request (async but not awaited)
    # making this hack because in serverless deployment(vercel) we cannot create async task, it kills the process
    # try:
    #     async with httpx.AsyncClient() as client:
    #         # Don't await this (fire-and-forget)
    #         client.post(BACKEND_DOMAIN + "api/leaderboard/recalculate")
    # except Exception:
    #     pass  # silently fail

async def get_top_players():
    raw_data = await db.leaderboard.find().sort("total_score", -1).limit(10).to_list(10)
    # Serialize ObjectId and return
    result = []
    print("raw data: ", raw_data)
    for player in raw_data:
        player["_id"] = str(player["_id"])  
        result.append(player)
    
    return result

async def get_user_rank(user_id: str):
    user_id = int(user_id)
    user = await db.leaderboard.find_one({"user_id": user_id}, {"rank": 1})
    return {"user_id": user_id, "rank": user["rank"] if user else None}


async def recalculate_all_ranks():
    cursor = db.leaderboard.find().sort("total_score", -1)
    bulk_ops = []
    rank = 1
    async for player in cursor:
        bulk_ops.append(UpdateOne(
            {"_id": player["_id"]},
            {"$set": {"rank": rank}}
        ))
        rank += 1

    if bulk_ops:
        await db.leaderboard.bulk_write(bulk_ops)
    return {"message": "Rankings updated", "count": rank - 1}
