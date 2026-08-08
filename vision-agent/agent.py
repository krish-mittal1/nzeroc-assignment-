from ultralytics import YOLO
import cv2
import requests
import uuid
from datetime import datetime, timezone

VIDEO_PATH = "clip2.mp4"

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO_PATH)
fps_estimate = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.release()

ZONE_FRACTION = (0.30, 0.50 , 0.55 , 0.95)

ZONE= (
    ZONE_FRACTION[0]*frame_width,
    ZONE_FRACTION[1]*frame_height,
    ZONE_FRACTION[2]*frame_width,
    ZONE_FRACTION[3]*frame_height
)
print(f"Frame size: {frame_width}x{frame_height}, computed ZONE: {ZONE}")

DWELL_THRESHOLD = 5
MOVEMENT_RESET_PX = 40
BACKEND_URL= "http://localhost:8000/events"
CAMERA_ID = "cam_01"

track_state = {}

def in_zone(cx, cy , zone):
    x1,y1,x2,y2 = zone
    return x1<= cx <=x2 and y1 <=cy <= y2

def post_event(track_id , zone_name, entry_time , exit_time, dwell_seconds):
    event={
        "id": f"evt_{uuid.uuid4().hex[:8]}",
        "camera_id":CAMERA_ID,
        "type": "zone_dwell_violation",
        "track_id": str(track_id),
        "zone": zone_name,
        "started_at": entry_time,
        "ended_at": exit_time,
        "dwell_seconds": dwell_seconds
    }
    try:
        resp= requests.post(BACKEND_URL, json=event, timeout=5)
        print(f"Posted event {event['id']} ->{resp.status_code}")
    except Exception as e:
        print(f"Failed to post event: {e}")


cap = cv2.VideoCapture(VIDEO_PATH)
fps_estimate = cap.get(cv2.CAP_PROP_FPS)
cap.release()

if not fps_estimate or fps_estimate <=0:
    print("Warning: could not detect fps from video, defaulting to 25")
    fps_estimate= 25

print(f"Detected video FPS: {fps_estimate}")


results = model.track(
    source="clip2.mp4",
    classes=[0],
    conf=0.5,
    persist=True,
    show = True,
    imgsz = 1280,
    stream= True
)


for frame_idx, r in enumerate(results):
    current_time = frame_idx / fps_estimate

    if r.boxes.id is None:
        continue

    for box, track_id in zip(r.boxes.xyxy, r.boxes.id):
        track_id = int(track_id)
        x1, y1,x2,y2 = box.tolist()
        cx , cy = (x1+x2)/2, (y1+y2)/2

        print(f"Frame {frame_idx} | Track ID: {track_id} | Center: ({cx:.0f}, {cy:.0f})")

        state = track_state.get(track_id, {"in_zone_since": None,"last_center": None, "reported":False})

        if in_zone(cx,cy, ZONE):
            if state["in_zone_since"] is None:
                state["in_zone_since"] = current_time
                state["reported"] = False
            else:
               if state["last_center"]:
                dist = ((cx-state["last_center"][0])**2 + (cy - state["last_center"][1])**2) **0.5
                if dist > MOVEMENT_RESET_PX:
                    state["in_zone_since"] = current_time
                    state["reported"] = False

            dwell= current_time - state["in_zone_since"]
            if dwell >= DWELL_THRESHOLD and not state["reported"]:
                entry_dt = datetime.now(timezone.utc)
                post_event(
                    track_id= track_id,
                    zone_name="restricted_a",
                    entry_time= entry_dt.isoformat().replace("+00:00","Z"),
                    exit_time= entry_dt.isoformat().replace("+00:00", "Z"),
                    dwell_seconds= round(dwell,1)
                )
                state["reported"] = True
        else:
            state["in_zone_since"] = None
            state["reported"] = False
        
        state["last_center"] = (cx,cy)
        track_state[track_id] = state

print("DONE processing video")