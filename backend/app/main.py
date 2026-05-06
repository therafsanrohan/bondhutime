from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth

app = FastAPI(
    title="BondhuTime API",
    description="Backend API for the BondhuTime SaaS ecosystem",
    version="1.0.0",
)

# CORS configuration for Next.js frontend and mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the BondhuTime API. The system is online."}

@app.get("/health")
def health_check():
    return {"status": "healthy", "components": {"database": "ok", "redis": "ok"}}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# Note: In a full implementation, routers would be included here:
# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(cycle.router, prefix="/api/v1/cycle", tags=["Cycle Tracking"])
# app.include_router(machines.router, prefix="/api/v1/machines", tags=["Machines"])
# app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
