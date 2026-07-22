import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { fetchHomeBootstrap } from "@/features/home/api/homeApi";
import type { DecisionRecord, EventItem } from "@/features/home/types";
import { buildStockPageViewModels } from "@/features/stock/adapters/stockPageViewModel";

function buildRelatedEvents(eventList: EventItem[], stockCode: string) {
  const directEvents = eventList.filter((event) => event.stockCode === stockCode);
  const firstDirectIndex = eventList.findIndex((event) => event.stockCode === stockCode);
  const contextSlice =
    firstDirectIndex > 0
      ? eventList.slice(Math.max(0, firstDirectIndex - 2), firstDirectIndex).filter((event) => !event.stockCode)
      : [];

  const merged = [...directEvents, ...contextSlice];
  return merged.length > 0 ? merged : eventList.slice(0, 3);
}

function pickStockName(relatedEvents: EventItem[], stockCode: string) {
  const directEvent = relatedEvents.find((event) => event.stockCode === stockCode);
  return directEvent?.summary.subject ?? `标的 ${stockCode}`;
}

function pickLatestRecord(recentDecisionRecords: DecisionRecord[], selectedEventId: string | null) {
  if (!selectedEventId) {
    return null;
  }
  return recentDecisionRecords.find((record) => record.eventId === selectedEventId) ?? null;
}

export function useStockPage() {
  const navigate = useNavigate();
  const { stockCode = "" } = useParams();

  const [eventList, setEventList] = useState<EventItem[]>([]);
  const [recentDecisionRecords, setRecentDecisionRecords] = useState<DecisionRecord[]>([]);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetchHomeBootstrap().then((payload) => {
      if (cancelled) {
        return;
      }
      const nextRelatedEvents = buildRelatedEvents(payload.events, stockCode);
      setEventList(payload.events);
      setRecentDecisionRecords(payload.decisionRecords);
      setSelectedEventId(nextRelatedEvents[0]?.summary.eventId ?? null);
    });

    return () => {
      cancelled = true;
    };
  }, [stockCode]);

  const relatedEvents = useMemo(() => buildRelatedEvents(eventList, stockCode), [eventList, stockCode]);
  const selectedEvent = useMemo(
    () => relatedEvents.find((event) => event.summary.eventId === selectedEventId) ?? relatedEvents[0] ?? null,
    [relatedEvents, selectedEventId],
  );
  const latestRecord = useMemo(
    () => pickLatestRecord(recentDecisionRecords, selectedEvent?.summary.eventId ?? null),
    [recentDecisionRecords, selectedEvent],
  );
  const stockName = useMemo(() => pickStockName(relatedEvents, stockCode), [relatedEvents, stockCode]);

  const viewModels = useMemo(
    () =>
      buildStockPageViewModels({
        stockCode,
        stockName,
        relatedEvents,
        selectedEvent,
        latestRecord,
      }),
    [stockCode, stockName, relatedEvents, selectedEvent, latestRecord],
  );

  return {
    stockCode,
    stockName,
    selectedEventId: selectedEvent?.summary.eventId ?? null,
    hasLoaded: eventList.length > 0,
    ...viewModels,
    handleSelectEvent: setSelectedEventId,
    handleBackHome: () => navigate("/"),
  };
}
