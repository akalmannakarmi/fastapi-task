from pathlib import Path
from app.core.taskiq import broker
from app.db.database import SessionLocal
from app.db.models import Task
from app.utils.customer import validate_file_columns, batch_and_insert
from time import time
import asyncio


@broker.task
async def process_file(task_id: int) -> None:
    print(f"Processing task {task_id} ...")
    start_time = time()
    for i in range(4):
        if i:
            print(f"Retrying task {task_id} ... ({i})")
        try:
            with SessionLocal() as db:
                task = db.get(Task, task_id)
                if not task:
                    raise Exception("Task Not Found")

                task.status = "processing"
                db.commit()

                file_path = Path("media/customer_file/") / task.file_name

            validate_file_columns(file_path)
            total, failed, succesful = batch_and_insert(file_path, task.user_id)

            with SessionLocal() as db:
                task = db.get(Task, task_id)
                task.status = "completed"
                task.total_records = total
                task.failed = failed
                task.succesful = succesful
                db.commit()

            end_time = time()
            duration = round(end_time - start_time, 2)
            print(f"Task {task_id} completed in {duration} seconds.")
            return
        except Exception as e:
            await asyncio.sleep(5)
            e.with_traceback()

    with SessionLocal() as db:
        task = db.get(Task, task_id)
        task.status = "failed"
        db.commit()
        print(f"Task {task_id} failed")
