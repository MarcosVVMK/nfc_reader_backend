from typing import Optional
from sqlalchemy.orm import Session

from .base_repository import BaseRepository
from ..models import User


class UserRepository(BaseRepository[User]):
    """Repository for User model with specific user operations"""
    
    def __init__(self, db_session: Session):
        super().__init__(db_session, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        return self.db_session.query(User).filter(User.email == email).first()
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.db_session.query(User).filter(User.email == email).first() is not None