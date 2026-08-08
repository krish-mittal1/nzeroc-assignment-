# NZeroC Take-Home Assessment — Krish Mittal

A three-layer pipeline: a vision agent that detects zone-dwell violations in a video clip, a FastAPI backend that stores/serves those events, and a Next.js frontend that displays them live.

## Screenshots

**Vision agent — detecting and tracking people, computing zone-dwell**
![Vision agent detection](docs/screenshots/vision-agent-detection.png)

**Backend — FastAPI Swagger docs (`POST /events`, `GET /events`)**
![Backend API docs](docs/screenshots/backend-swagger.png)

**Frontend — live event feed pulling from the backend**
![Frontend live events](docs/screenshots/frontend-events.png)


## Stack
- **Vision agent**: Python, OpenCV, Ultralytics YOLOv8n (nano), ByteTrack (via `model.track()`)
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Next.js (App Router), TypeScript, Tailwind CSS

## How to run (in order, on a clean machine)

### 1. Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows; use `source .venv/bin/activate` on Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Runs on `http://localhost:8000`. Interactive docs at `/docs`.

### 2. Vision agent
```bash
cd vision-agent
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python agent.py
```
Requires the backend running first — it posts detected violations live via HTTP.

**Note:** test video clips are not committed to the repo (see `.gitignore` —
`*.mp4` excluded to keep the repo small). Place any short clip of people
standing/working in one spot as `clip1.mp4` inside `vision-agent/`, or update
`VIDEO_PATH` in `agent.py` to point at your own file. The YOLOv8n model
weights (`yolov8n.pt`) are also not committed — they auto-download (~6MB) on
first run.

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on `http://localhost:3000`. Needs a `.env.local` file (see below).

### Frontend environment variables
Create `frontend/.env.local`:

### What does each piece does

### What each piece does (plain-language)

- **YOLOv8n** — detects people in each video frame and puts a box around them. It is small and fast.
- **ByteTrack** — gives each person an ID and keeps the same ID while they move across frames. This helps us track how long someone stays in an area.
- **OpenCV** — reads the video frame by frame and gets basic video information like FPS and frame size.
- **FastAPI** — handles communication between the AI system, database, and frontend. It receives violation events and sends them to the frontend.
- **SQLAlchemy + SQLite** — SQLAlchemy helps the Python code work with the database, while SQLite stores the data in a simple database file.
- **Next.js + TypeScript** — used to build the frontend where violation events are displayed with filters and pagination.
- **Tailwind CSS** — used to style the frontend and make the page look clean.

