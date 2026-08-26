from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from models.user import User
from schemas.user import UserRead

# Creating users lives in routers/auth.py (`register`). This router only reads.
# All routes require a logged-in user.
router = APIRouter(prefix="/users", tags=["users"])


# NOTE: /me must be declared BEFORE /{user_id}, otherwise FastAPI would treat
# the literal "me" as a user_id and hit the wrong route.
@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    # The logged-in user's own profile — always safe to return.
    return current_user


@router.get("/", response_model=list[UserRead])
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
