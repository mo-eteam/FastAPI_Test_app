from fastapi import APIRouter, Depends
from ..security import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/")
async def list_categories(current_user: str = Depends(get_current_user)):
    return {"message": "Categories list", "user": current_user}
