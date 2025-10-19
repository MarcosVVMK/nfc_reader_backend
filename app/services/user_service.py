from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .base_service import BaseService
from ..repositories.user_repository import UserRepository
from ..schemas import UserCreate, UserUpdate, UserResponse
from ..models import User


class UserService(BaseService):
    """Service for user business logic"""
    
    def __init__(self, db_session: Session):
        super().__init__(db_session)
        self.user_repository = UserRepository(db_session)
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user with email already exists
        if self.user_repository.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user_dict = user_data.model_dump()
        return self.user_repository.create(user_dict)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return self.user_repository.get_all(skip=skip, limit=limit)
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """Update user"""
        if not self.user_repository.exists(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Check if email is being updated and if it already exists
        if 'email' in update_data:
            existing_user = self.user_repository.get_by_email(update_data['email'])
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        updated_user = self.user_repository.update(user_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    
    def delete_user(self, user_id: int) -> None:
        """Delete user"""
        if not self.user_repository.delete(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )