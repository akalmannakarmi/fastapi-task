from pydantic import BaseModel, EmailStr

class TaskOut(BaseModel):
    id: int
    status: str
    file_name: str
    queued_task_id: str
    total_records: int
    failed: int
    succesful: int

    class Config():
        from_attributes = True