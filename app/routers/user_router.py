from fastapi import APIRouter , BackgroundTasks
from schemas.user_schema import UserCreate , UserResponse
from services.user_service import UserService
from tasks.email_tasks import send_welcome_email

router = APIRouter(prefix="/users")

# To create a user with background task to send welcome email
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    new_user = UserService.create_user(user.dict())
    background_tasks.add_task(send_welcome_email, new_user["email"])
    return new_user

# To get user by ID with error handling for not found user
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return UserService.get_user(user_id)

# To get all users
@router.get("/", response_model=list[UserResponse])
def get_users():
    return UserService.get_all_users()