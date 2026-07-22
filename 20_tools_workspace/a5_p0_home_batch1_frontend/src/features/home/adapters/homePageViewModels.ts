import {
  createDecisionRecordFormViewModel,
  createExplanationCardViewModel,
  createEventStreamViewModel,
  createHomeHeroViewModel,
  createHomeSidebarViewModel,
  createMainWorkspaceViewModel,
  createSelectedEventSummaryViewModel,
  createStockSearchBarViewModel,
  type DecisionRecordFormViewModel,
  type EventStreamCardViewModel,
  type ExplanationCardViewModel,
  type HomeHeroViewModel,
  type HomeSidebarViewModel,
  type MainWorkspaceViewModel,
  type SelectedEventSummaryViewModel,
  type StockSearchBarViewModel,
} from "@/features/home/adapters/homeViewModel";
import type {
  DecisionDraft,
  DecisionRecord,
  EventItem,
  FinanceDisclosureContext,
  HomeWorkspaceState,
} from "@/features/home/types";

interface CreateHomePageViewModelsParams {
  eventList: EventItem[];
  queuedEvents: EventItem[];
  recentDecisionRecords: DecisionRecord[];
  selectedEvent: EventItem | null;
  homeWorkspaceState: HomeWorkspaceState;
  homeRecordDraft: DecisionDraft;
  financeDisclosureContext: FinanceDisclosureContext;
  marketSummary: string;
  holdingRiskHint: string;
}

export interface HomePageViewModels {
  heroViewModel: HomeHeroViewModel;
  eventStreamViewModel: EventStreamCardViewModel[];
  sidebarViewModel: HomeSidebarViewModel;
  stockSearchBarViewModel: StockSearchBarViewModel;
  mainWorkspaceViewModel: MainWorkspaceViewModel;
  decisionRecordFormViewModel: DecisionRecordFormViewModel;
  selectedEventSummaryViewModel: SelectedEventSummaryViewModel | null;
  explanationCardViewModel: ExplanationCardViewModel | null;
}

export function createHomePageViewModels(params: CreateHomePageViewModelsParams): HomePageViewModels {
  const {
    eventList,
    queuedEvents,
    recentDecisionRecords,
    selectedEvent,
    homeWorkspaceState,
    homeRecordDraft,
    financeDisclosureContext,
    marketSummary,
    holdingRiskHint,
  } = params;

  return {
    heroViewModel: createHomeHeroViewModel({
      totalEvents: eventList.length,
      queuedEventCount: queuedEvents.length,
      marketSummary,
      holdingRiskHint,
      disclosureLabel: financeDisclosureContext.label,
    }),
    eventStreamViewModel: createEventStreamViewModel(eventList),
    sidebarViewModel: createHomeSidebarViewModel({
      queuedEvents,
      recentDecisionRecords,
      financeDisclosureContext,
    }),
    stockSearchBarViewModel: createStockSearchBarViewModel(),
    mainWorkspaceViewModel: createMainWorkspaceViewModel(),
    decisionRecordFormViewModel: createDecisionRecordFormViewModel(homeRecordDraft.eventId),
    selectedEventSummaryViewModel: selectedEvent
      ? createSelectedEventSummaryViewModel(selectedEvent, homeWorkspaceState)
      : null,
    explanationCardViewModel: selectedEvent ? createExplanationCardViewModel(selectedEvent) : null,
  };
}
