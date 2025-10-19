from abc import ABC
from sqlalchemy.orm import Session


class BaseService(ABC):
    """Base service class for business logic"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session