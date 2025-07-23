from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Define app first
app = FastAPI()

# ✅ Add CORS middleware after app is created
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],  # adjust based on your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Then import and include your routers
from app.routes import router
app.include_router(router, prefix="/api/leaderboard")
