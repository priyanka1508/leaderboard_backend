# Gaming Leaderboard Backend – FastAPI + MongoDB (Serverless on Vercel)

A scalable backend service for a gaming leaderboard system, capable of handling millions of user score submissions and concurrent access patterns. Built with FastAPI, MongoDB, and designed for serverless deployment on Vercel.

---

## API Endpoints

### 1. Submit Score

**POST /api/leaderboard/submit**

Submit a new score for a user.

- Payload:
  ```json
  {
    "user_id": 1234,
    "score": 2500
  }
Behavior:

- Inserts a new game session

- Atomically updates total score in the leaderboard

- Triggers async rank recalculation (fire-and-forget)

### 2. Get Top Players
**GET /api/leaderboard/top**

Returns top 10 users sorted by total score (desc)

- Currently reads directly from DB

- Future-ready for caching with Redis

### 3. Get User Rank
**GET /api/leaderboard/rank/{user_id}**

Returns the current rank of a given user

- Computed from pre-ranked leaderboard collection

### 4. Recalculate Ranks (Internal)
**POST /api/leaderboard/recalculate**

Recalculates and updates ranks for all users in the leaderboard

- Triggered asynchronously from /submit


### Optimizations Implemented
| Area             | Description                                                                |
| ---------------- | -------------------------------------------------------------------------- |
| Atomic Updates   | Score updates are done using MongoDB's `$inc` and `upsert` for concurrency |
| Async Fire-off   | Rank recalculation is triggered but not awaited, preventing API latency    |
| Indexing         | Expected to index `user_id`, `total_score` in leaderboard                  |
| Serverless Ready | Fully deployable to Vercel Python Functions                                |
| Redis Caching    | Planned (see future section)                                               |


## Future Enhancements

Due to time constraints, the following were scoped out but remain planned:

### Redis Caching
- Cache `GET /top` (10s TTL)
- Cache per-user rank (`GET /rank/{user_id}`)

### Batch-Based Rank Calculation
- Offload ranking to a worker every N seconds
- Use Redis queue or task broker (e.g., Celery)

### Monitoring with New Relic
- Already integrated with `newrelic.agent` (env-based config)
- Will use custom events for API latency profiling


### Local Setup Instructions
1. Clone the repo
```
git clone https://github.com/your-username/leaderboard-backend.git
cd leaderboard-backend
```
2. Create virtual environment & install dependencies
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Setup environment variables
Create a .env file (or set via shell):
```
MONGO_URL=mongodb+srv://<user>:<pass>@cluster.mongodb.net/db
NEW_RELIC_LICENSE_KEY=your_key
NEW_RELIC_APP_NAME=leaderboard-backend
NEW_RELIC_LOG=stdout
```

4. Run locally
```
uvicorn app.main:app --reload --port 8000
Visit http://localhost:8000/docs for interactive Swagger API.
```

### Deploying to Vercel
1. Push this repo to GitHub
2. Connect repo on https://vercel.com/
3. Add the following Environment Variables in the project settings:

| Key                      | Value               |
| ------------------------ | ------------------- |
| MONGO\_URL               | Your MongoDB URI    |
| NEW\_RELIC\_LICENSE\_KEY | Your New Relic key  |
| NEW\_RELIC\_APP\_NAME    | leaderboard-backend |
| NEW\_RELIC\_LOG          | stdout              |


Vercel will handle serverless deployment automatically.
