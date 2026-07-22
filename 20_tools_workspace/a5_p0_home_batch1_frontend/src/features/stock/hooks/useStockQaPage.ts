import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";

import { fetchHomeBootstrap } from "@/features/home/api/homeApi";
import type { DecisionRecord, EventItem } from "@/features/home/types";

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

function buildQuestionFocusedAnswer(
  selectedQuestion: string,
  selectedEvent: EventItem,
  latestRecord: DecisionRecord | null,
) {
  switch (selectedQuestion) {
    case "影响推演具体在说什么":
      return {
        explanationSupplement: selectedEvent.explanation.impact,
        recordReminder: latestRecord
          ? `最近记录仍是「${latestRecord.action} / ${latestRecord.reasonTag}」，返回标的页时优先核对这次影响推演是否改变原处理节奏。`
          : "当前还没有直接绑定记录，返回标的页后优先看这次影响推演是否值得补一条观察备注。",
      };
    case "历史类比对应了哪段过去情况":
      return {
        explanationSupplement: selectedEvent.explanation.historyAnalogy,
        recordReminder: latestRecord
          ? `最近记录可作为历史类比的落点参考：当前记录是「${latestRecord.action} / ${latestRecord.reasonTag} / ${latestRecord.horizon}」。`
          : "当前没有直接绑定记录，因此历史类比只回链事件字段，不延伸出新的动作结论。",
      };
    case "上次为什么这样记录":
      return {
        explanationSupplement: latestRecord
          ? `上次之所以记录为「${latestRecord.action}」，当时使用的是「${latestRecord.reasonTag} / ${latestRecord.horizon}」口径；备注是“${latestRecord.note}”。`
          : "当前没有直接绑定记录，因此只能回链当前事件解释，不能补写一条并不存在的历史处理原因。",
        recordReminder: latestRecord
          ? `如果要继续追问这条记录，可返回标的页在“最近决策记录区”继续补充备注，而不是在问答页改动作。`
          : "当前没有可回看的原始记录，返回标的页后可先确认是否需要形成第一条记录。",
      };
    case "下一次复查点要看什么":
      return {
        explanationSupplement: selectedEvent.explanation.nextReviewPoint,
        recordReminder: latestRecord
          ? `返回标的页后，可把这次复查点与最近记录「${latestRecord.action}」一起看，避免解释和记录脱链。`
          : "当前还没有直接绑定记录，返回标的页后可先围绕复查点补充一条观察备注。",
      };
    case "这次事件为什么触发":
    default:
      return {
        explanationSupplement: selectedEvent.explanation.logic,
        recordReminder: latestRecord
          ? `最近记录为「${latestRecord.action} / ${latestRecord.reasonTag} / ${latestRecord.horizon}」，返回标的页时优先核对当前触发逻辑是否仍支撑原记录。`
          : "当前没有直接绑定记录，因此这次回答只解释事件为什么触发，不外推新的处理结论。",
      };
  }
}

function buildAnswerBlocks(selectedQuestion: string, selectedEvent: EventItem | null, latestRecord: DecisionRecord | null) {
  if (!selectedEvent) {
    return [];
  }

  const focusedAnswer = buildQuestionFocusedAnswer(selectedQuestion, selectedEvent, latestRecord);

  return [
    {
      title: "问题复述",
      content: `当前问题是“${selectedQuestion}”，它绑定在事件「${selectedEvent.summary.title}」上。`,
    },
    {
      title: "当前事件回链",
      content: `本次回答只基于当前事件的触发逻辑、影响推演、历史类比与下一次复查点字段；最近记录${
        latestRecord ? "也已纳入回看参考。" : "当前没有直接绑定记录，因此只回链事件字段。"
      }`,
    },
    {
      title: "解释补充",
      content: focusedAnswer.explanationSupplement,
    },
    {
      title: "记录/回看提醒",
      content: focusedAnswer.recordReminder,
    },
    {
      title: "金融限制提醒",
      content: "still_need_evidence，当前仍受相对基准限制；这里只做解释增强，不输出自由荐股或价格预测。",
    },
  ];
}

export function useStockQaPage() {
  const navigate = useNavigate();
  const { stockCode = "" } = useParams();
  const [searchParams] = useSearchParams();
  const requestedEventId = searchParams.get("eventId");

  const [eventList, setEventList] = useState<EventItem[]>([]);
  const [recentDecisionRecords, setRecentDecisionRecords] = useState<DecisionRecord[]>([]);
  const [selectedQuestion, setSelectedQuestion] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetchHomeBootstrap().then((payload) => {
      if (cancelled) {
        return;
      }
      setEventList(payload.events);
      setRecentDecisionRecords(payload.decisionRecords);
    });

    return () => {
      cancelled = true;
    };
  }, []);

  const relatedEvents = useMemo(() => buildRelatedEvents(eventList, stockCode), [eventList, stockCode]);
  const selectedEvent = useMemo(
    () => relatedEvents.find((event) => event.summary.eventId === requestedEventId) ?? relatedEvents[0] ?? null,
    [relatedEvents, requestedEventId],
  );
  const stockName = useMemo(() => pickStockName(relatedEvents, stockCode), [relatedEvents, stockCode]);
  const latestRecord = useMemo(
    () => pickLatestRecord(recentDecisionRecords, selectedEvent?.summary.eventId ?? null),
    [recentDecisionRecords, selectedEvent],
  );

  const recommendedQuestions = useMemo(
    () =>
      selectedEvent
        ? [
            "这次事件为什么触发",
            "影响推演具体在说什么",
            "历史类比对应了哪段过去情况",
            "上次为什么这样记录",
            "下一次复查点要看什么",
          ]
        : [],
    [selectedEvent],
  );

  useEffect(() => {
    setSelectedQuestion((previous) => {
      if (recommendedQuestions.length === 0) {
        return null;
      }
      return previous && recommendedQuestions.includes(previous) ? previous : recommendedQuestions[0];
    });
  }, [recommendedQuestions]);

  const answerBlocks = useMemo(
    () => buildAnswerBlocks(selectedQuestion ?? "", selectedEvent, latestRecord),
    [selectedQuestion, selectedEvent, latestRecord],
  );

  return {
    stockCode,
    stockName,
    selectedEventTitle: selectedEvent?.summary.title ?? "当前事件未锁定",
    selectedEventSubject: selectedEvent?.summary.subject ?? "",
    hasLoaded: eventList.length > 0,
    recommendedQuestions,
    selectedQuestion,
    answerBlocks,
    latestRecord,
    stillNeedEvidenceLabel: "still_need_evidence",
    setSelectedQuestion,
    handleBackStock: () => navigate(`/stock/${stockCode}?eventId=${encodeURIComponent(selectedEvent?.summary.eventId ?? "")}`),
  };
}
