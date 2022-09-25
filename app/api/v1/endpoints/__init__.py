from fastapi import APIRouter

from app.api.v1.endpoints import auth, board, task, user

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(board.router, prefix="/board", tags=["board"])
api_router.include_router(task.router, prefix="/task", tags=["task"])
