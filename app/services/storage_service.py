import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from PIL import Image
import io


class LocalStorageService:
    
    def __init__(self, base_upload_dir: str = "static/uploads"):
        self.base_upload_dir = Path(base_upload_dir)
        self.base_upload_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_user_directory(self, user_id: int) -> Path:
        user_dir = self.base_upload_dir / "users" / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    def _validate_image(self, file: UploadFile) -> None:
        
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Formato inválido. Permitidos: JPEG, PNG, WebP"
            )
        
        ext = file.filename.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
            raise HTTPException(status_code=400, detail="Extensão de arquivo inválida")
    
    async def save_profile_picture(
        self, 
        user_id: int, 
        file: UploadFile,
        max_size_mb: int = 5
    ) -> dict:
                
        self._validate_image(file)
        
        contents = await file.read()
        file_size = len(contents)
        
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_size > max_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Máximo: {max_size_mb}MB"
            )
        
        try:
            img = Image.open(io.BytesIO(contents))
            
            max_dimension = 1024
            if img.width > max_dimension or img.height > max_dimension:
                img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            output = io.BytesIO()
            img_format = 'JPEG' if file.content_type == 'image/jpeg' else 'PNG'
            img.save(output, format=img_format, quality=85, optimize=True)
            contents = output.getvalue()
            file_size = len(contents)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao processar imagem: {str(e)}")
        
        ext = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        
        user_dir = self._get_user_directory(user_id)
        file_path = user_dir / unique_filename
        
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        return {
            "filename": unique_filename,
            "original_filename": file.filename,
            "filepath": str(file_path.relative_to(self.base_upload_dir.parent)),
            "file_size": file_size,
            "mime_type": file.content_type
        }
    
    def delete_file(self, filepath: str) -> None:
        try:
            file_path = Path(filepath)
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            print(f"Erro ao deletar arquivo: {e}")
    
    def delete_user_pictures(self, user_id: int) -> None:
        user_dir = self.base_upload_dir / "users" / str(user_id)
        if user_dir.exists():
            shutil.rmtree(user_dir)