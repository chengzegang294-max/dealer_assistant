export type HoldingRelation = "持仓相关" | "关注相关" | "其它";
export type ProcessStatus = "pending" | "done";
export type HomeWorkspaceState = "empty" | "selected" | "editing" | "submitted";
export type DecisionAction = "继续观察" | "加入跟踪" | "暂缓动作";
export type ReasonTag = "环境顺风" | "热点承接" | "资金背书" | "信号待确认" | "风险升温";
export type Horizon = "日内" | "1-3天" | "1周";

export interface FinanceDisclosureContext {
  label: string;
  detail: string;
}

export interface EventSummary {
  eventId: string;
  title: string;
  subject: string;
  occurredAt: string;
  holdingRelation: HoldingRelation;
  processStatus: ProcessStatus;
  disclosureFlag: string;
}

export interface ExplanationPayload {
  eventId: string;
  title: string;
  subject: string;
  logic: string;
  impact: string;
  historyAnalogy: string;
  nextReviewPoint: string;
}

export interface EventItem {
  summary: EventSummary;
  explanation: ExplanationPayload;
  sourceCard: string;
  stockCode?: string;
  group: HoldingRelation;
}

export interface DecisionDraft {
  eventId: string | null;
  action: DecisionAction | "";
  reasonTag: ReasonTag | "";
  horizon: Horizon | "";
  note: string;
}

export type DecisionDraftChangeHandler = <K extends keyof DecisionDraft>(key: K, value: DecisionDraft[K]) => void;

export interface SubmitEcho {
  eventId: string;
  title: string;
  action: DecisionAction;
  submittedAt: string;
  summary: string;
}

export interface DecisionRecord {
  id: string;
  eventId: string;
  title: string;
  action: DecisionAction;
  reasonTag: ReasonTag;
  horizon: Horizon;
  note: string;
  submittedAt: string;
}

export const decisionActionOptions: DecisionAction[] = ["继续观察", "加入跟踪", "暂缓动作"];
export const reasonTagOptions: ReasonTag[] = ["环境顺风", "热点承接", "资金背书", "信号待确认", "风险升温"];
export const horizonOptions: Horizon[] = ["日内", "1-3天", "1周"];
