from app.db import db
from bson import ObjectId

async def submit_score(user_id: str, score: int):
    await db.game_sessions.insert_one({
        "user_id": int(user_id),
        "score": score
    })

    await db.leaderboard.update_one(
        {"user_id": int(user_id)},
        {"$inc": {"total_score": score}},
        upsert=True
    )

    # Recalculate rank (simplified, use better logic later)
    cursor = db.leaderboard.find().sort("total_score", -1)
    rank = 1
    async for entry in cursor:
        await db.leaderboard.update_one({"_id": entry["_id"]}, {"$set": {"rank": rank}})
        rank += 1

async def get_top_players():
    raw_data = await db.leaderboard.find().sort("total_score", -1).limit(10).to_list(10)
    # Serialize ObjectId and return
    result = []
    for player in raw_data:
        player["_id"] = str(player["_id"])  
        result.append(player)
    
    return result

async def get_user_rank(user_id: str):
    result = await db.leaderboard.find_one({"user_id": int(user_id)})
    if result:
        result["_id"] = str(result["_id"])  
        return {"user_id": user_id, "rank": result["rank"]}
    return {"user_id": user_id, "rank": None}
