import {
  financeDisclosureContext,
  holdingRiskHint,
  marketSummary,
} from "@/features/home/fixtures/sixCardEvents";
import { useNavigate } from "react-router-dom";
import { createHomePageViewModels } from "@/features/home/adapters/homePageViewModels";
import type {
  EventStreamPanelProps,
  HomeSidebarProps,
  MainWorkspacePanelProps,
  StockSearchBarProps,
} from "@/features/home/contracts/homeSectionProps";
import { useHomeWorkspace } from "@/features/home/hooks/useHomeWorkspace";

export function useHomePage() {
  const navigate = useNavigate();
  const workspace = useHomeWorkspace();

  function handleOpenStockPage(stockCode: string) {
    workspace.handleOpenStockPage(stockCode);
    const normalizedCode = stockCode.trim();
    if (!normalizedCode) {
      return;
    }
    navigate(`/stock/${normalizedCode}`);
  }

  function handleOpenFinanceDisclosure() {
    const target = document.getElementById("finance-disclosure-note");
    target?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  const viewModels = createHomePageViewModels({
    eventList: workspace.eventList,
    queuedEvents: workspace.queuedEvents,
    recentDecisionRecords: workspace.recentDecisionRecords,
    selectedEvent: workspace.selectedEvent,
    homeWorkspaceState: workspace.homeWorkspaceState,
    homeRecordDraft: workspace.homeRecordDraft,
    financeDisclosureContext,
    marketSummary,
    holdingRiskHint,
  });

  const eventStreamPanelProps: EventStreamPanelProps = {
    eventCards: viewModels.eventStreamViewModel,
    selectedEventId: workspace.selectedEventId,
    onSelectEvent: workspace.handleSelectEvent,
  };

  const stockSearchBarProps: StockSearchBarProps = {
    viewModel: viewModels.stockSearchBarViewModel,
    content: {
      searchDraft: workspace.searchDraft,
      searchActionEcho: workspace.searchActionEcho,
    },
    actions: {
      onSearchDraftChange: workspace.setSearchDraft,
      onOpenStockPage: handleOpenStockPage,
      onOpenFinanceDisclosure: handleOpenFinanceDisclosure,
    },
  };

  const mainWorkspacePanelProps: MainWorkspacePanelProps = {
    viewModel: viewModels.mainWorkspaceViewModel,
    content: {
      selectedEventSummaryViewModel: viewModels.selectedEventSummaryViewModel,
      explanationCardViewModel: viewModels.explanationCardViewModel,
      decisionRecordFormViewModel: viewModels.decisionRecordFormViewModel,
      homeRecordDraft: workspace.homeRecordDraft,
      latestSubmitEcho: workspace.latestSubmitEcho,
      formError: workspace.formError,
    },
    actions: {
      onChangeDecisionDraft: workspace.handleChangeDecisionDraft,
      onSubmitDecision: workspace.handleSubmitDecision,
      onRetrySubmitDecision: workspace.handleRetrySubmitDecision,
      onOpenStockPage: handleOpenStockPage,
    },
  };

  const homeSidebarProps: HomeSidebarProps = {
    viewModel: viewModels.sidebarViewModel,
    actions: {
      onSelectEvent: workspace.handleSelectEvent,
    },
  };

  return {
    ...workspace,
    ...viewModels,
    eventStreamPanelProps,
    stockSearchBarProps,
    mainWorkspacePanelProps,
    homeSidebarProps,
    handleOpenStockPage,
    handleOpenFinanceDisclosure,
  };
}
