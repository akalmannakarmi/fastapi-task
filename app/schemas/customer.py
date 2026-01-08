from pydantic import BaseModel, EmailStr

class TaskOut(BaseModel):
    task_id: str
    status: str
    file_name: str