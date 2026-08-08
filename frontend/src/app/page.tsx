"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchEvents } from "@/lib/api";
import { Event } from "@/types/event";
import ModeBanner from "@/components/ModeBanner";

export default function Home() {
  const [events, setEvents] = useState<Event[]>([]);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);

  const [typeFilter, setTypeFilter] = useState("");
  const [zoneFilter, setZoneFilter] = useState("");

  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadEvents = useCallback(
    async (opts: { reset: boolean; cursor?: string | null }) => {
      const isFirstLoad = opts.reset;
      isFirstLoad ? setLoading(true) : setLoadingMore(true);
      setError(null);

      try {
        const data = await fetchEvents({
          limit: 10,
          cursor: opts.cursor ?? undefined,
          type: typeFilter || undefined,
          zone: zoneFilter || undefined,
        });

        setEvents((prev) => (isFirstLoad ? data.items : [...prev, ...data.items]));
        setNextCursor(data.next_cursor);
        setHasMore(data.has_more);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load events");
      } finally {
        setLoading(false);
        setLoadingMore(false);
      }
    },
    [typeFilter, zoneFilter]
  );

  // Initial load, and reload whenever filters change
  useEffect(() => {
    loadEvents({ reset: true });
  }, [loadEvents]);

  function handleLoadMore() {
    if (nextCursor) {
      loadEvents({ reset: false, cursor: nextCursor });
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-zinc-50">
      <ModeBanner />

      <main className="flex-1 w-full max-w-4xl mx-auto px-6 py-10">
        <h1 className="text-2xl font-semibold text-zinc-900 mb-6">
          Safety Events
        </h1>

        {/* Filters */}
        <div className="flex gap-4 mb-6">
          <input
            type="text"
            placeholder="Filter by type (e.g. zone_dwell_violation)"
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="border border-zinc-300 rounded px-3 py-2 text-sm flex-1"
          />
          <input
            type="text"
            placeholder="Filter by zone (e.g. restricted_a)"
            value={zoneFilter}
            onChange={(e) => setZoneFilter(e.target.value)}
            className="border border-zinc-300 rounded px-3 py-2 text-sm flex-1"
          />
        </div>

        {/* Loading state (first load only) */}
        {loading && (
          <div className="text-center py-12 text-zinc-500">Loading events…</div>
        )}

        {/* Error state */}
        {!loading && error && (
          <div className="text-center py-12 text-red-600 bg-red-50 rounded border border-red-200">
            Error: {error}
          </div>
        )}

        {/* Empty state */}
        {!loading && !error && events.length === 0 && (
          <div className="text-center py-12 text-zinc-500">
            No events found.
          </div>
        )}

        {/* Event list */}
        {!loading && !error && events.length > 0 && (
          <div className="space-y-3">
            {events.map((event) => (
              <div
                key={event.id}
                className="border border-zinc-200 bg-white rounded p-4 shadow-sm"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-zinc-900">{event.type}</p>
                    <p className="text-sm text-zinc-500">
                      Zone: {event.zone} · Camera: {event.camera_id} · Track:{" "}
                      {event.track_id}
                    </p>
                  </div>
                  <span className="text-sm text-zinc-600">
                    {event.dwell_seconds}s dwell
                  </span>
                </div>
                <p className="text-xs text-zinc-400 mt-2">
                  {new Date(event.started_at).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        )}

        {/* Load more */}
        {!loading && !error && hasMore && (
          <div className="text-center mt-6">
            <button
              onClick={handleLoadMore}
              disabled={loadingMore}
              className="px-4 py-2 bg-zinc-900 text-white rounded text-sm disabled:opacity-50"
            >
              {loadingMore ? "Loading…" : "Load more"}
            </button>
          </div>
        )}
      </main>
    </div>
  );
}