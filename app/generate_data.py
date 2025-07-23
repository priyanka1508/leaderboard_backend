import random
import argparse
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING
from tqdm import tqdm

def generate_users(db, num_users):
    users = []
    for i in range(1, num_users + 1):
        users.append({"username": f"user_{i}"})
    db.users.insert_many(users)


def generate_game_sessions(db, num_sessions, num_users):
    sessions = []
    for _ in tqdm(range(num_sessions)):
        session = {
            "user_id": random.randint(1, num_users),
            "score": random.randint(1, 10000),
            "game_mode": "solo" if random.random() > 0.5 else "team",
            "timestamp": datetime.utcnow() - timedelta(days=random.randint(0, 365))
        }
        sessions.append(session)
        if len(sessions) >= 10000:
            db.game_sessions.insert_many(sessions)
            sessions = []
    if sessions:
        db.game_sessions.insert_many(sessions)


def populate_leaderboard(db):
    pipeline = [
        {"$group": {"_id": "$user_id", "total_score": {"$sum": "$score"}}},
        {"$sort": {"total_score": -1}}
    ]
    leaderboard = list(db.game_sessions.aggregate(pipeline))

    leaderboard_docs = []
    for rank, entry in enumerate(leaderboard, start=1):
        leaderboard_docs.append({
            "user_id": entry["_id"],
            "total_score": entry["total_score"],
            "rank": rank
        })

    db.leaderboard.delete_many({})
    db.leaderboard.insert_many(leaderboard_docs)


def main():
    parser = argparse.ArgumentParser(description="Generate data for MongoDB Leaderboard App")
    parser.add_argument('--uri', type=str, required=True, help='MongoDB connection URI')
    parser.add_argument('--users', type=int, default=1000, help='Number of users to generate')
    parser.add_argument('--sessions', type=int, default=10000, help='Number of game sessions to generate')
    args = parser.parse_args()

    client = MongoClient(args.uri)
    db = client.get_default_database()

    print("🛠 Connected to MongoDB")

    db.users.delete_many({})
    db.game_sessions.delete_many({})
    db.leaderboard.delete_many({})

    generate_users(db, args.users)
    generate_game_sessions(db, args.sessions, args.users)
    populate_leaderboard(db)


if __name__ == "__main__":
    main()
