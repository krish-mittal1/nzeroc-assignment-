from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.track(
    source = "clip1.mp4",
    classes= [0],
    conf = 0.5,
    persist = True,
    show = True,
    imgsz = 1280
)
