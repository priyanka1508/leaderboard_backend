import os
import newrelic.agent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from newrelic.api.asgi_application import ASGIApplicationWrapper


# os.environ["NEW_RELIC_APP_NAME"] = os.getenv("NEW_RELIC_APP_NAME")
# os.environ["NEW_RELIC_LICENSE_KEY"] = os.getenv("NEW_RELIC_LICENSE_KEY")
# os.environ["NEW_RELIC_LOG"] = "stdout"
# os.environ["NEW_RELIC_DISTRIBUTED_TRACING_ENABLED"] = "true"
# os.environ["NEW_RELIC_ENABLED"] = "true"

# newrelic.agent.initialize()

app = FastAPI()
# app = ASGIApplicationWrapper(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://leaderboard-ui-murex.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routes import router
app.include_router(router, prefix="/api/leaderboard")
