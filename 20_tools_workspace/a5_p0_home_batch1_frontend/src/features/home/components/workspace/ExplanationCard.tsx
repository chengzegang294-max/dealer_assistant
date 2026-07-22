import { InfoBlock } from "@/features/home/components/shared";
import type { ExplanationCardViewModel } from "@/features/home/adapters/homeViewModel";

interface ExplanationCardProps {
  viewModel: ExplanationCardViewModel;
  onOpenStockPage: (stockCode: string) => void;
}

export function ExplanationCard(props: ExplanationCardProps) {
  const { viewModel, onOpenStockPage } = props;

  return (
    <article className="rounded-3xl border border-white/10 bg-slate-950/40 p-5">
      <p className="text-xs font-medium uppercase tracking-[0.22em] text-slate-400">{viewModel.eyebrow}</p>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        {viewModel.blocks.map((block) => (
          <InfoBlock key={block.title} title={block.title} content={block.content} />
        ))}
      </div>
      {viewModel.stockCode ? (
        <button
          type="button"
          onClick={() => onOpenStockPage(viewModel.stockCode)}
          className="mt-4 rounded-2xl border border-cyan-400/30 px-4 py-2 text-sm font-medium text-cyan-100 transition hover:bg-cyan-500/10"
        >
          {viewModel.openStockActionLabel}
        </button>
      ) : null}
    </article>
  );
}
