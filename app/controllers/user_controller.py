from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services.user_service import UserService
from ..schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency injection for UserService"""
    return UserService(db)

@router.get("/api/v1/users/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service)):
    """Get all users with pagination"""
    return user_service.get_users(skip=skip, limit=limit)

@router.post("/api/v1/users/", response_model=UserResponse)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    """Create a new user"""
    return user_service.create_user(user)

@router.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Get a user by ID"""
    return user_service.get_user_by_id(user_id)

@router.put("/api/v1/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, user_service: UserService = Depends(get_user_service)):
    """Update a user"""
    return user_service.update_user(user_id, user_update)

@router.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Delete a user"""
    user_service.delete_user(user_id)
    return None


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency injection for UserService"""
    return UserService(db)


@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, 
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    return user_service.create_user(user)


@router.get("/users/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    user_service: UserService = Depends(get_user_service)
):
    """Get all users with pagination"""
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int, 
    user_service: UserService = Depends(get_user_service)
):
    """Get a user by ID"""
    return user_service.get_user_by_id(user_id)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    user_service: UserService = Depends(get_user_service)
):
    """Update a user"""
    return user_service.update_user(user_id, user_update)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, 
    user_service: UserService = Depends(get_user_service)
):
    """Delete a user"""
    user_service.delete_user(user_id)
    return None