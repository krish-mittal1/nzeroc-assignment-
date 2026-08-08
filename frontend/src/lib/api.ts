import { PaginatedEventsResponse } from "@/types/event";

const API_URL = process.env.NEXT_PUBLIC_API_URL

export interface FetchEvenetsParams{
    limit?: number;
    cursor?: string | null;
    type?: string;
    zone?: string;
}

export async function fetchEvents(
    params: FetchEvenetsParams ={}
): Promise<PaginatedEventsResponse>{
    if(!API_URL){
        throw new Error(
            "NEXT_PUBLIC_API_URL is not set check your .env.local file."
        );
    }

    const searchParams = new URLSearchParams();
    if (params.limit) searchParams.set("limit", String(params.limit));
    if (params.cursor) searchParams.set("cursor", params.cursor);
    if (params.type) searchParams.set("type", params.type);
    if (params.zone) searchParams.set("zone", params.zone);

    const url = `${API_URL}/events?${searchParams.toString()}`;

    const res = await fetch(url);

    if(!res.ok){
        throw new Error(`Failed to fetch events : ${res.status} ${res.statusText}`);
    }

    return res.json();
}