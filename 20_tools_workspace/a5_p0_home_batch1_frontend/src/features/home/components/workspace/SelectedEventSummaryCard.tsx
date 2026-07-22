import type { SelectedEventSummaryViewModel } from "@/features/home/adapters/homeViewModel";
import { statusLabel, statusTone } from "@/features/home/utils/statusPresentation";

interface SelectedEventSummaryCardProps {
  viewModel: SelectedEventSummaryViewModel;
}

export function SelectedEventSummaryCard(props: SelectedEventSummaryCardProps) {
  const { viewModel } = props;

  return (
    <article className="rounded-3xl border border-white/10 bg-slate-950/40 p-4">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.22em] text-slate-400">{viewModel.eyebrow}</p>
          <h2 className="mt-2 text-xl font-semibold text-white">{viewModel.title}</h2>
          <p className="mt-2 text-sm text-slate-300">{viewModel.metaLine}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <span className={`rounded-full px-3 py-1 text-xs ${statusTone(viewModel.processStatus)}`}>
            {statusLabel(viewModel.processStatus)}
          </span>
          <span className="rounded-full bg-fuchsia-500/10 px-3 py-1 text-xs text-fuchsia-200">{viewModel.disclosureFlag}</span>
          <span className="rounded-full bg-white/5 px-3 py-1 text-xs text-slate-300">{viewModel.workspaceState}</span>
        </div>
      </div>
    </article>
  );
}
