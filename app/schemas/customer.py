from pydantic import BaseModel


class TaskOut(BaseModel):
    id: int
    status: str
    file_name: str
    queued_task_id: str

    class Config:
        from_attributes = True


class MetricsOut(BaseModel):
    id: int
    total_records: int
    failed: int
    succesful: int

    class Config:
        from_attributes = True
