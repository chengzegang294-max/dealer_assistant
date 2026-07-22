import type { EventStreamCardViewModel, HomeSidebarViewModel } from "@/features/home/adapters/homeViewModelTypes";
import type { DecisionRecord, EventItem, FinanceDisclosureContext } from "@/features/home/types";

export function createEventStreamViewModel(eventList: EventItem[]): EventStreamCardViewModel[] {
  return eventList.map((event) => ({
    eventId: event.summary.eventId,
    title: event.summary.title,
    subject: event.summary.subject,
    occurredAt: event.summary.occurredAt,
    holdingRelation: event.summary.holdingRelation,
    disclosureFlag: event.summary.disclosureFlag,
    sourceCard: event.sourceCard,
    processStatus: event.summary.processStatus,
  }));
}

export function createHomeSidebarViewModel(params: {
  queuedEvents: EventItem[];
  recentDecisionRecords: DecisionRecord[];
  financeDisclosureContext: FinanceDisclosureContext;
}): HomeSidebarViewModel {
  const { queuedEvents, recentDecisionRecords, financeDisclosureContext } = params;

  return {
    queuedEventCards: queuedEvents.map((event) => ({
      eventId: event.summary.eventId,
      title: event.summary.title,
      subject: event.summary.subject,
      occurredAt: event.summary.occurredAt,
    })),
    queuedEmptyMessage: "当前待处理队列为空，说明本轮事件都已经进入记录状态。",
    recentRecordCards: recentDecisionRecords.map((record) => ({
      id: record.id,
      title: record.title,
      summaryLine: `${record.action} · ${record.reasonTag} · ${record.horizon}`,
      note: record.note,
      submittedAt: record.submittedAt,
    })),
    financeDisclosureLabel: financeDisclosureContext.label,
    financeDisclosureDetail: financeDisclosureContext.detail,
  };
}
