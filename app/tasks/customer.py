from app.core.taskiq import broker
from app.db.database import SessionLocal
from app.db.models import Task
import asyncio

@broker.task
async def process_file(task_id) -> None:
    
    with SessionLocal() as db:
        task: Task|None = db.query(Task).get(task_id)
        if not task:
            return
        
        task.status = "processing"
        db.commit()

        # Processing here
        await asyncio.sleep(5.5)

        task.status = "completed"
        db.commit()
    # Also add metrics later