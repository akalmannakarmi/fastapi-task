from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.schemas.customer import *
from app.api.deps import get_db,get_current_user
from app.db.models import User
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
from datetime import datetime,timezone

router = APIRouter()

TEMPLATE_FILE = "media/template.csv"
UPLOAD_DIR = Path("media/customer_file/")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/template")
def template(_=Depends(get_current_user)):
    return FileResponse(
        path=TEMPLATE_FILE,
        filename="template.csv",
        media_type="text/csv"
    )

@router.post("/upload",response_model=TaskOut)
def upload(file:UploadFile = File(...), user:User=Depends(get_current_user)):
    ext = Path(file.filename).suffix.lower()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    new_name = f"{user.id}_{timestamp}{ext}"

    if ext not in {".csv", ".xls", ".xlsx"}:
        raise HTTPException(400, "Invalid file type")
    
    file_path = UPLOAD_DIR / new_name
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Schedule task
    task_id = "asd"

    return {"task_id":task_id,"status":"queued","file_name":new_name}

# @router.post("/progress",response_model=TaskOut)
# def progress(task_id:str,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
#     pass


# @router.post("/metics",response_model=MetricsOut)
# def metrics(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
#     pass


