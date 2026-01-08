from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.schemas.customer import TaskOut, MetricsOut
from app.api.deps import get_db,get_current_user
from app.db.models import User, Task
from app.tasks.customer import process_file
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
from datetime import datetime,timezone
from sqlalchemy.orm import Session

router = APIRouter()

TEMPLATE_FILE = "static/template.csv"
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
async def upload(file:UploadFile = File(...), user:User=Depends(get_current_user), db:Session = Depends(get_db)):
    ext = Path(file.filename).suffix.lower()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    new_name = f"{user.id}_{timestamp}{ext}"

    if ext not in {".csv", ".xls", ".xlsx"}:
        raise HTTPException(400, "Invalid file type")
    
    file_path = UPLOAD_DIR / new_name
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Queue task
    task = Task(
        status = "queued",
        file_name = new_name,
        user_id = user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    queued_task = await process_file.kiq(str(task.id))
    task.queued_task_id = queued_task.task_id
    db.commit()

    return task

@router.get("/progress",response_model=TaskOut)
def progress(task_id:int,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    task = db.query(Task).get(task_id)

    if not task:
        raise HTTPException(404,"Task not found")
    elif task.user_id != user.id:
        raise HTTPException(403,"Access Denied")
    
    return task


@router.get("/metrics",response_model=MetricsOut)
def metrics(task_id:int,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    task = db.query(Task).get(task_id)

    if not task:
        raise HTTPException(404,"Task not found")
    elif task.user_id != user.id:
        raise HTTPException(403,"Access Denied")
    elif task.status not in ["completed","failed"]:
        raise HTTPException(400,"Task hasnt processed yet")
    
    return task


