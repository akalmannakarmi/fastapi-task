from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.customer import *
from app.api.deps import get_db,get_current_user

router = APIRouter()

@router.get("/template")
def template(user:User=Depends(get_current_user)):
    pass

@router.post("/upload",response_model=UploadRes)
def upload(user:User=Depends(get_current_user)):
    pass

@router.post("/progress",response_model=TaskOut)
def progress(task_id:str,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    pass


@router.post("/metics",response_model=MetricsOut)
def metrics(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    pass


