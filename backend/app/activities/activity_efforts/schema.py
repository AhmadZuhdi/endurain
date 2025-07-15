from pydantic import BaseModel

class RelativeEffort(BaseModel):
    
    relative_effort: int | None = None
    activity_id: int
    date: str