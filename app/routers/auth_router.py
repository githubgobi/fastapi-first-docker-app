from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.deps import get_current_user
from core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = fake_user_db.get(form_data.username)

    # if not user or not verify_password(form_data.password, user["password"]):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")

    # token = create_access_token({"sub": user["username"]})
    token = create_access_token({"sub": form_data.username})

    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile")
async def get_profile(current_user: str = Depends(get_current_user)):
    return {"user": current_user}