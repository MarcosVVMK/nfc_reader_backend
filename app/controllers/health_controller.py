from fastapi import APIRouter

router = APIRouter()

@router.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

@router.get("/api/v1/health/db")
def health_db_check():
    # Aqui você pode adicionar lógica para verificar o banco
    return {"db_status": "ok"}
