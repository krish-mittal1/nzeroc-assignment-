from pydantic import ConfigDict
from pydantic import BaseModel

class EventIn(BaseModel):
    id:str
    camera_id : str
    type:str
    track_id: str
    zone: str
    started_at : str
    ended_at : str
    dwell_seconds: int

class EventOut(EventIn):
    model_config = ConfigDict(from_attributes=True)