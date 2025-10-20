from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.user_picture import UserPicture
from app.schemas.user_picture_schema import UserPictureResponse, UserPictureList
from app.services.storage_service import LocalStorageService

router = APIRouter()


@router.post("/{user_id}/pictures", response_model=UserPictureResponse, status_code=status.HTTP_201_CREATED)
async def upload_profile_picture(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    storage = LocalStorageService()
    
    file_info = await storage.save_profile_picture(user_id, file)
    
    db.query(UserPicture).filter(
        UserPicture.user_id == user_id,
        UserPicture.is_active == True
    ).update({"is_active": False})
    
    new_picture = UserPicture(
        user_id=user_id,
        filename=file_info["filename"],
        filepath=file_info["filepath"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"],
        is_active=True
    )
    
    db.add(new_picture)
    db.commit()
    db.refresh(new_picture)
    
    return new_picture


@router.get("/{user_id}/pictures", response_model=List[UserPictureList])
def list_user_pictures(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    pictures = db.query(UserPicture).filter(
        UserPicture.user_id == user_id
    ).order_by(UserPicture.uploaded_at.desc()).all()
    
    return pictures


@router.get("/{user_id}/pictures/current", response_model=UserPictureResponse)
def get_current_picture(user_id: int, db: Session = Depends(get_db)):
    
    picture = db.query(UserPicture).filter(
        UserPicture.user_id == user_id,
        UserPicture.is_active == True
    ).first()
    
    if not picture:
        raise HTTPException(status_code=404, detail="Usuário sem foto de perfil")
    
    return picture


@router.put("/{user_id}/pictures/{picture_id}/activate", response_model=UserPictureResponse)
def set_active_picture(user_id: int, picture_id: int, db: Session = Depends(get_db)):
    
    picture = db.query(UserPicture).filter(
        UserPicture.id == picture_id,
        UserPicture.user_id == user_id
    ).first()
    
    if not picture:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    db.query(UserPicture).filter(
        UserPicture.user_id == user_id
    ).update({"is_active": False})
    
    picture.is_active = True
    db.commit()
    db.refresh(picture)
    
    return picture


@router.delete("/{user_id}/pictures/{picture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_picture(user_id: int, picture_id: int, db: Session = Depends(get_db)):
    
    picture = db.query(UserPicture).filter(
        UserPicture.id == picture_id,
        UserPicture.user_id == user_id
    ).first()
    
    if not picture:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    storage = LocalStorageService()
    storage.delete_file(picture.filepath)
    
    db.delete(picture)
    db.commit()


@router.delete("/{user_id}/pictures", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_pictures(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    storage = LocalStorageService()
    storage.delete_user_pictures(user_id)
    
    db.query(UserPicture).filter(UserPicture.user_id == user_id).delete()
    db.commit()