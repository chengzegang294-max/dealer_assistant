import type {
  DecisionAction,
  EventItem,
  Horizon,
  HomeWorkspaceState,
  ReasonTag,
} from "@/features/home/types";

export interface HomeHeroViewModelInput {
  totalEvents: number;
  queuedEventCount: number;
  marketSummary: string;
  holdingRiskHint: string;
  disclosureLabel: string;
}

export interface HomeHeroViewModel {
  eyebrow: string;
  title: string;
  description: string;
  axisTitle: string;
  axisSummary: string;
  totalEvents: number;
  queuedEventCount: number;
  statusMetrics: Array<{
    title: string;
    value: string;
    hint: string;
  }>;
}

export interface EventStreamCardViewModel {
  eventId: string;
  title: string;
  subject: string;
  occurredAt: string;
  holdingRelation: string;
  disclosureFlag: string;
  sourceCard: string;
  processStatus: EventItem["summary"]["processStatus"];
}

export interface HomeSidebarViewModel {
  queuedEventCards: Array<{
    eventId: string;
    title: string;
    subject: string;
    occurredAt: string;
  }>;
  queuedEmptyMessage: string;
  recentRecordCards: Array<{
    id: string;
    title: string;
    summaryLine: string;
    note: string;
    submittedAt: string;
  }>;
  financeDisclosureLabel: string;
  financeDisclosureDetail: string;
}

export interface StockSearchBarViewModel {
  entryLabel: string;
  placeholder: string;
  openActionLabel: string;
  disclosureButtonLabel: string;
}

export interface MainWorkspaceViewModel {
  eyebrow: string;
  title: string;
  description: string;
  emptyStateTitle: string;
  emptyStateDescription: string;
}

export interface SelectedEventSummaryViewModel {
  eyebrow: string;
  title: string;
  metaLine: string;
  processStatus: EventItem["summary"]["processStatus"];
  disclosureFlag: string;
  workspaceState: HomeWorkspaceState;
}

export interface ExplanationCardViewModel {
  eyebrow: string;
  blocks: Array<{
    title: string;
    content: string;
  }>;
  openStockActionLabel: string | null;
  stockCode: string | null;
}

export interface DecisionRecordFormViewModel {
  eyebrow: string;
  description: string;
  draftEventLabel: string;
  actionField: {
    label: string;
    placeholder: string;
    options: DecisionAction[];
  };
  reasonTagField: {
    label: string;
    placeholder: string;
    options: ReasonTag[];
  };
  horizonField: {
    label: string;
    placeholder: string;
    options: Horizon[];
  };
  noteLabel: string;
  notePlaceholder: string;
  submitButtonLabel: string;
  retryButtonLabel: string;
}
