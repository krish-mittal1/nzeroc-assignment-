from sqlalchemy import Column , String, Integer

from .database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String , primary_key=True , index=True)
    camera_id = Column(String , nullable=False)
    type = Column(String , nullable=False , index = True)
    track_id= Column(String , nullable = False)
    zone = Column(String , nullable = False , index= True)
    started_at= Column(String , nullable=False)
    ended_at= Column(String , nullable=False)
    dwell_seconds= Column(Integer, nullable=False)