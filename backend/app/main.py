from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import hcp, interactions, follow_ups, agent

app = FastAPI(
    title="AI-First CRM — HCP Module",
    description="Log Interaction Screen for pharma field representatives",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(hcp.router, prefix="/api", tags=["HCPs"])
app.include_router(interactions.router, prefix="/api", tags=["Interactions"])
app.include_router(follow_ups.router, prefix="/api", tags=["Follow-Ups"])
app.include_router(agent.router, prefix="/api", tags=["Agent"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "AI-First CRM HCP Module API"}
# trigger reload
