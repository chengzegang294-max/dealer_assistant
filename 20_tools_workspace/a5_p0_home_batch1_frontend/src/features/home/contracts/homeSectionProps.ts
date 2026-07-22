import type {
  DecisionRecordFormViewModel,
  EventStreamCardViewModel,
  ExplanationCardViewModel,
  HomeSidebarViewModel,
  MainWorkspaceViewModel,
  SelectedEventSummaryViewModel,
  StockSearchBarViewModel,
} from "@/features/home/adapters/homeViewModel";
import type {
  DecisionDraft,
  DecisionDraftChangeHandler,
  SubmitEcho,
} from "@/features/home/types";

export interface EventStreamPanelProps {
  eventCards: EventStreamCardViewModel[];
  selectedEventId: string | null;
  onSelectEvent: (eventId: string) => void;
}

export interface StockSearchBarProps {
  viewModel: StockSearchBarViewModel;
  content: {
    searchDraft: string;
    searchActionEcho: string | null;
  };
  actions: {
    onSearchDraftChange: (value: string) => void;
    onOpenStockPage: (stockCode: string) => void;
    onOpenFinanceDisclosure: () => void;
  };
}

export interface MainWorkspacePanelContent {
  selectedEventSummaryViewModel: SelectedEventSummaryViewModel | null;
  explanationCardViewModel: ExplanationCardViewModel | null;
  decisionRecordFormViewModel: DecisionRecordFormViewModel;
  homeRecordDraft: DecisionDraft;
  latestSubmitEcho: SubmitEcho | null;
  formError: string | null;
}

export interface MainWorkspacePanelActions {
  onChangeDecisionDraft: DecisionDraftChangeHandler;
  onSubmitDecision: () => void;
  onRetrySubmitDecision: () => void;
  onOpenStockPage: (stockCode: string) => void;
}

export interface MainWorkspacePanelProps {
  viewModel: MainWorkspaceViewModel;
  content: MainWorkspacePanelContent;
  actions: MainWorkspacePanelActions;
}

export interface HomeSidebarProps {
  viewModel: HomeSidebarViewModel;
  actions: {
    onSelectEvent: (eventId: string) => void;
  };
}
