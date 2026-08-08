export interface Event {
  id: string;
  camera_id: string;
  type: string;
  track_id: string;
  zone: string;
  started_at: string;
  ended_at: string;
  dwell_seconds: number;
}

export interface PaginatedEventsResponse {
  items: Event[];
  next_cursor: string | null;
  has_more: boolean;
}