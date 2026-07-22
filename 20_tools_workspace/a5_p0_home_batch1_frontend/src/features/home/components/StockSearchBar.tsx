import type { StockSearchBarProps } from "@/features/home/contracts/homeSectionProps";

export function StockSearchBar(props: StockSearchBarProps) {
  const { viewModel, content, actions } = props;

  return (
    <section className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
        <label className="flex-1">
          <span className="mb-2 block text-xs font-medium uppercase tracking-[0.22em] text-slate-400">
            {viewModel.entryLabel}
          </span>
          <input
            value={content.searchDraft}
            onChange={(event) => actions.onSearchDraftChange(event.target.value)}
            placeholder={viewModel.placeholder}
            className="w-full rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 text-sm text-white outline-none ring-0 transition focus:border-cyan-400/50"
          />
        </label>
        <div className="flex gap-3">
          <button
            type="button"
            onClick={() => actions.onOpenStockPage(content.searchDraft)}
            className="rounded-2xl bg-cyan-400 px-4 py-3 text-sm font-medium text-slate-950 transition hover:bg-cyan-300"
          >
            {viewModel.openActionLabel}
          </button>
          <button
            type="button"
            onClick={actions.onOpenFinanceDisclosure}
            className="rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:border-cyan-400/40 hover:text-white"
          >
            {viewModel.disclosureButtonLabel}
          </button>
        </div>
      </div>
      {content.searchActionEcho ? <p className="mt-3 text-sm text-cyan-200">{content.searchActionEcho}</p> : null}
    </section>
  );
}
