# main.py
from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import auth, receipt

# entrypoint
app = FastAPI()

# including routers
app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(receipt.router, prefix='/receipts', tags=['receipts'])

# applying migrations to db
Base.metadata.create_all(bind=engine)
