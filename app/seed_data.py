import asyncio
import random
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection (adjust if needed)
client = AsyncIOMotorClient("mongodb+srv://priyanka:phulwari@cluster1.kiaexwt.mongodb.net")
db = client["leaderboardgame"]

async def seed():
    await db.game_sessions.delete_many({})
    await db.leaderboard.delete_many({})

    users = [f"user{i}" for i in range(1, 21)]

    leaderboard_entries = []

    for user_id in users:
        score = random.randint(10, 100)
        total_score = random.randint(100, 1000)

        # Insert into game_sessions
        await db.game_sessions.insert_one({
            "user_id": user_id,
            "score": score
        })

        # Collect for leaderboard
        leaderboard_entries.append({
            "user_id": user_id,
            "total_score": total_score
        })

    # Sort by total_score descending and assign ranks
    leaderboard_entries.sort(key=lambda x: x["total_score"], reverse=True)

    for rank, entry in enumerate(leaderboard_entries, start=1):
        entry["rank"] = rank
        await db.leaderboard.insert_one(entry)

    print("✅ 20 users inserted into game_sessions and leaderboard with ranks")

asyncio.run(seed())
