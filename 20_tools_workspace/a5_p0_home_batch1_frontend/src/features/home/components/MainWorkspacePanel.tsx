import type { MainWorkspacePanelProps } from "@/features/home/contracts/homeSectionProps";
import { SectionHeader } from "@/features/home/components/shared";
import { DecisionRecordForm } from "@/features/home/components/workspace/DecisionRecordForm";
import { ExplanationCard } from "@/features/home/components/workspace/ExplanationCard";
import { SelectedEventSummaryCard } from "@/features/home/components/workspace/SelectedEventSummaryCard";
import { SubmitEchoPanel } from "@/features/home/components/workspace/SubmitEchoPanel";

export function MainWorkspacePanel(props: MainWorkspacePanelProps) {
  const { content, actions } = props;
  const hasSelectedEvent = content.selectedEventSummaryViewModel && content.explanationCardViewModel;

  return (
    <section className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 shadow-xl shadow-slate-950/20">
      <SectionHeader
        eyebrow={props.viewModel.eyebrow}
        title={props.viewModel.title}
        description={props.viewModel.description}
      />

      {!hasSelectedEvent ? (
        <div className="mt-4 rounded-3xl border border-dashed border-white/10 bg-slate-950/40 p-10 text-center">
          <p className="text-lg font-medium text-white">{props.viewModel.emptyStateTitle}</p>
          <p className="mt-2 text-sm text-slate-400">{props.viewModel.emptyStateDescription}</p>
        </div>
      ) : (
        <div className="mt-4 flex flex-col gap-4">
          <SelectedEventSummaryCard viewModel={content.selectedEventSummaryViewModel} />
          <ExplanationCard viewModel={content.explanationCardViewModel} onOpenStockPage={actions.onOpenStockPage} />
          <DecisionRecordForm
            viewModel={content.decisionRecordFormViewModel}
            homeRecordDraft={content.homeRecordDraft}
            formError={content.formError}
            onChangeDecisionDraft={actions.onChangeDecisionDraft}
            onSubmitDecision={actions.onSubmitDecision}
            onRetrySubmitDecision={actions.onRetrySubmitDecision}
          />
          <SubmitEchoPanel latestSubmitEcho={content.latestSubmitEcho} />
        </div>
      )}
    </section>
  );
}
