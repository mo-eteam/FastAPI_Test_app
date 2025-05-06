from fastapi import APIRouter, Depends, HTTPException
from ..security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
