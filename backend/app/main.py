from fastapi import FastAPI , Depends , HTTPException , Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional 

from .database import engine , Base , SessionLocal
from .models import Event
from .schemas import EventIn,EventOut

Base.metadata.create_all(bind=engine)
app=FastAPI(title="Nzeroc event API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/events", response_model=EventOut)
def create_event(event : EventIn, db: Session=Depends(get_db)):
    existing = db.query(Event).filter(Event.id == event.id).first()
    if existing:
        return existing

    db_event=Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events")
def get_events(
    limit: int = Query(default=10 , ge=1 , le=50),
    cursor: Optional[str] = None,
    type: Optional[str] = None,
    zone: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)

    if type:
        query= query.filter(Event.type == type)
    if zone:
        query = query.filter(Event.zone == zone)
    if cursor:
        query = query.filter(Event.started_at < cursor)
    
    query = query.order_by(Event.started_at.desc())

    items = query.limit(limit+1).all()
    has_more = len(items) >limit
    if has_more:
        items=items[:limit]
        next_cursor = items[-1].started_at
    else:
        next_cursor = None 
    
    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more
    }


