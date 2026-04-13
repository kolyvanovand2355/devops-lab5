from fastapi import APIRouter, HTTPException, status
from src.schemas.user import CreateUser, UserInfo
from src.fake_db import db

router = APIRouter()

@router.get("", response_model=UserInfo)
async def get_user(email: str):
    user = db.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUser):
    if db.get_user_by_email(data.email) is not None:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    db.create_user(data.name, data.email)
    return db.get_user_by_email(data.email)['id']

