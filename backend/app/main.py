from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, investors, commitments
from app.db.database import Base, engine

# Create database tables


app = FastAPI(swagger_ui_parameters={"deepLinking": False})
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins, you can specify specific domains here if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(investors.router, prefix="/api/investors", tags=["Investors"])
app.include_router(commitments.router, prefix="/api/commitments", tags=["Commitments"])
