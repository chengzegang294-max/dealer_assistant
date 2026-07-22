import { StatusMetric } from "@/features/home/components/shared";

import type { HomeHeroViewModel } from "@/features/home/adapters/homeViewModel";

type HomeHeroProps = HomeHeroViewModel;

export function HomeHero(props: HomeHeroProps) {
  return (
    <div className="flex flex-col gap-5">
      <div className="flex flex-col gap-2 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.24em] text-cyan-300/80">{props.eyebrow}</p>
          <h1 className="mt-2 text-3xl font-semibold text-white">{props.title}</h1>
          <p className="mt-2 max-w-3xl text-sm text-slate-300">{props.description}</p>
        </div>
        <div className="rounded-2xl border border-cyan-400/20 bg-cyan-500/10 px-4 py-3 text-sm text-cyan-100">
          <p className="font-medium">{props.axisTitle}</p>
          <p className="mt-1 text-cyan-100/80">{props.axisSummary}</p>
        </div>
      </div>

      <section className="grid gap-4 lg:grid-cols-[1.25fr_1fr_0.95fr]">
        {props.statusMetrics.map((metric) => (
          <StatusMetric key={metric.title} title={metric.title} value={metric.value} hint={metric.hint} />
        ))}
      </section>
    </div>
  );
}
