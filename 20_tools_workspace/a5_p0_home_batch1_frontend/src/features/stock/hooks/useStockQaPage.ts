import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";

import { fetchHomeBootstrap } from "@/features/home/api/homeApi";
import type { DecisionRecord, EventItem } from "@/features/home/types";

interface StockQaQuestionDefinition {
  groupTitle: string;
  groupDescription: string;
  question: string;
  sourceFieldLabels: string[];
  buildCoreAnswer: (selectedEvent: EventItem, latestRecord: DecisionRecord | null) => string;
  buildNextActions: (latestRecord: DecisionRecord | null) => string[];
}

interface StockQaQuestionGroupViewModel {
  title: string;
  description: string;
  questions: string[];
}

interface StockQaAnswerViewModel {
  question: string;
  groupTitle: string;
  sourceFieldLabels: string[];
  sourceSummary: string;
  coreAnswer: string;
  nextActions: string[];
  limitReminder: string;
}

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

function buildQuestionDefinitions(): StockQaQuestionDefinition[] {
  return [
    {
      groupTitle: "解释补充组",
      groupDescription: "先把当前事件的解释字段读透，不扩成泛市场聊天。",
      question: "这次事件为什么触发",
      sourceFieldLabels: ["触发逻辑", "当前事件标题"],
      buildCoreAnswer: (selectedEvent) => selectedEvent.explanation.logic,
      buildNextActions: (latestRecord) =>
        latestRecord
          ? ["回到标的页继续看解释", "查看最近记录", "核对原记录是否仍成立"]
          : ["回到标的页继续看解释", "确认是否需要形成第一条记录"],
    },
    {
      groupTitle: "解释补充组",
      groupDescription: "先把当前事件的解释字段读透，不扩成泛市场聊天。",
      question: "影响推演具体在说什么",
      sourceFieldLabels: ["影响推演", "当前事件标题"],
      buildCoreAnswer: (selectedEvent) => selectedEvent.explanation.impact,
      buildNextActions: (latestRecord) =>
        latestRecord
          ? ["回到标的页继续看解释", "查看最近记录", "对照影响推演补充备注"]
          : ["回到标的页继续看解释", "评估是否要补一条观察备注"],
    },
    {
      groupTitle: "解释补充组",
      groupDescription: "先把当前事件的解释字段读透，不扩成泛市场聊天。",
      question: "历史类比对应了哪段过去情况",
      sourceFieldLabels: ["历史类比", "当前事件标题"],
      buildCoreAnswer: (selectedEvent) => selectedEvent.explanation.historyAnalogy,
      buildNextActions: (latestRecord) =>
        latestRecord
          ? ["回到标的页继续看解释", "查看最近记录", "对照历史类比回看原记录"]
          : ["回到标的页继续看解释", "保持只回链事件字段，不补写不存在的旧记录"],
    },
    {
      groupTitle: "记录复盘组",
      groupDescription: "把当前事件和最近记录接起来，但不在问答页直接改动作。",
      question: "上次为什么这样记录",
      sourceFieldLabels: ["最近动作", "理由标签", "预期周期", "备注"],
      buildCoreAnswer: (_selectedEvent, latestRecord) =>
        latestRecord
          ? `上次之所以记录为「${latestRecord.action}」，当时使用的是「${latestRecord.reasonTag} / ${latestRecord.horizon}」口径；备注是“${latestRecord.note}”。`
          : "当前没有直接绑定记录，因此这里只能提示你返回标的页确认是否需要先形成一条最小记录。",
      buildNextActions: (latestRecord) =>
        latestRecord
          ? ["查看最近记录", "补充这次记录", "回到标的页继续看解释"]
          : ["回到标的页继续看解释", "确认是否需要先形成记录"],
    },
    {
      groupTitle: "记录复盘组",
      groupDescription: "把当前事件和最近记录接起来，但不在问答页直接改动作。",
      question: "这次还需要补充记录什么",
      sourceFieldLabels: ["最近动作", "备注", "当前事件标题", "触发逻辑"],
      buildCoreAnswer: (selectedEvent, latestRecord) =>
        latestRecord
          ? `如果要补充记录，优先补“这次事件和原记录之间新出现了什么变化”。当前可回链「${selectedEvent.summary.title}」的触发逻辑，并围绕原备注“${latestRecord.note}”补新变化。`
          : `当前还没有直接绑定记录，因此先不要在问答页硬补历史动作；返回标的页后，可围绕事件「${selectedEvent.summary.title}」决定是否形成第一条观察记录。`,
      buildNextActions: (latestRecord) =>
        latestRecord
          ? ["补充这次记录", "查看最近记录", "回到标的页继续看解释"]
          : ["回到标的页继续看解释", "确认是否需要形成第一条记录"],
    },
    {
      groupTitle: "下一步关注组",
      groupDescription: "看完回答后，明确该回哪里继续走主路径。",
      question: "下一次复查点要看什么",
      sourceFieldLabels: ["下一次复查点", "当前事件标题"],
      buildCoreAnswer: (selectedEvent) => selectedEvent.explanation.nextReviewPoint,
      buildNextActions: (latestRecord) =>
        latestRecord
          ? ["回到标的页继续看解释", "查看最近记录", "把复查点和原记录一起看"]
          : ["回到标的页继续看解释", "围绕复查点补一条观察备注"],
    },
    {
      groupTitle: "下一步关注组",
      groupDescription: "看完回答后，明确该回哪里继续走主路径。",
      question: "如果还不确定，应该回到哪里继续看",
      sourceFieldLabels: ["当前解释区", "最近决策记录区", "still_need_evidence"],
      buildCoreAnswer: (selectedEvent, latestRecord) =>
        latestRecord
          ? `如果看完仍不确定，先回到标的页的“当前解释区”重看「${selectedEvent.summary.title}」，再到“最近决策记录区”核对原记录，不要在问答页直接放大成新结论。`
          : `如果看完仍不确定，先回到标的页的“当前解释区”重看「${selectedEvent.summary.title}」，当前没有直接绑定记录，因此先不要补写不存在的处理历史。`,
      buildNextActions: (latestRecord) =>
        latestRecord
          ? ["回到标的页继续看解释", "查看最近记录", "必要时补充这次记录"]
          : ["回到标的页继续看解释", "保持 still_need_evidence，不外推新结论"],
    },
  ];
}

function buildQuestionGroups(questionDefinitions: StockQaQuestionDefinition[]): StockQaQuestionGroupViewModel[] {
  return questionDefinitions.reduce<StockQaQuestionGroupViewModel[]>((groups, definition) => {
    const currentGroup = groups.find((group) => group.title === definition.groupTitle);
    if (currentGroup) {
      currentGroup.questions.push(definition.question);
      return groups;
    }

    groups.push({
      title: definition.groupTitle,
      description: definition.groupDescription,
      questions: [definition.question],
    });
    return groups;
  }, []);
}

function buildAnswerViewModel(
  selectedQuestionDefinition: StockQaQuestionDefinition | null,
  selectedEvent: EventItem | null,
  latestRecord: DecisionRecord | null,
): StockQaAnswerViewModel | null {
  if (!selectedQuestionDefinition || !selectedEvent) {
    return null;
  }

  return {
    question: selectedQuestionDefinition.question,
    groupTitle: selectedQuestionDefinition.groupTitle,
    sourceFieldLabels: selectedQuestionDefinition.sourceFieldLabels,
    sourceSummary: `当前回答回链到事件「${selectedEvent.summary.title}」；对象是「${selectedEvent.summary.subject}」；${
      latestRecord ? "最近记录也已纳入回看参考。" : "当前没有直接绑定记录，因此只回链事件字段。"
    }`,
    coreAnswer: selectedQuestionDefinition.buildCoreAnswer(selectedEvent, latestRecord),
    nextActions: selectedQuestionDefinition.buildNextActions(latestRecord),
    limitReminder: "still_need_evidence，当前仍受相对基准限制；这里只做解释增强，不输出自由荐股或价格预测。",
  };
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
  const questionDefinitions = useMemo(() => buildQuestionDefinitions(), []);
  const questionGroups = useMemo(() => buildQuestionGroups(questionDefinitions), [questionDefinitions]);

  const recommendedQuestions = useMemo(
    () => questionDefinitions.map((definition) => definition.question),
    [questionDefinitions],
  );

  useEffect(() => {
    setSelectedQuestion((previous) => {
      if (recommendedQuestions.length === 0) {
        return null;
      }
      return previous && recommendedQuestions.includes(previous) ? previous : recommendedQuestions[0];
    });
  }, [recommendedQuestions]);

  const selectedQuestionDefinition = useMemo(
    () => questionDefinitions.find((definition) => definition.question === selectedQuestion) ?? null,
    [questionDefinitions, selectedQuestion],
  );

  const answerViewModel = useMemo(
    () => buildAnswerViewModel(selectedQuestionDefinition, selectedEvent, latestRecord),
    [selectedQuestionDefinition, selectedEvent, latestRecord],
  );

  return {
    stockCode,
    stockName,
    selectedEventTitle: selectedEvent?.summary.title ?? "当前事件未锁定",
    selectedEventSubject: selectedEvent?.summary.subject ?? "",
    hasLoaded: eventList.length > 0,
    questionGroups,
    recommendedQuestions,
    selectedQuestion,
    answerViewModel,
    latestRecord,
    stillNeedEvidenceLabel: "still_need_evidence",
    setSelectedQuestion,
    handleBackStock: () => navigate(`/stock/${stockCode}?eventId=${encodeURIComponent(selectedEvent?.summary.eventId ?? "")}`),
  };
}
