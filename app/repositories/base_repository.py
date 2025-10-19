from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Type, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta

T = TypeVar('T', bound=DeclarativeMeta)


class BaseRepository(Generic[T], ABC):

    def __init__(self, db_session: Session, model: Type[T]):
        self.db_session = db_session
        self.model = model
    
    def create(self, obj_data: Dict[str, Any]) -> T:
        db_obj = self.model(**obj_data)
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, obj_id: int) -> Optional[T]:
        return self.db_session.query(self.model).filter(self.model.id == obj_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db_session.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, obj_id: int, update_data: Dict[str, Any]) -> Optional[T]:
        obj = self.get_by_id(obj_id)
        if obj:
            for field, value in update_data.items():
                setattr(obj, field, value)
            self.db_session.commit()
            self.db_session.refresh(obj)
        return obj
    
    def delete(self, obj_id: int) -> bool:
        """Delete object by ID"""
        obj = self.get_by_id(obj_id)
        if obj:
            self.db_session.delete(obj)
            self.db_session.commit()
            return True
        return False
    
    def exists(self, obj_id: int) -> bool:
        return self.db_session.query(self.model).filter(self.model.id == obj_id).first() is not None