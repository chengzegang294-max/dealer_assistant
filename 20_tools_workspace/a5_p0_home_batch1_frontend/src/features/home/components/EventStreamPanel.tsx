import type { EventStreamPanelProps } from "@/features/home/contracts/homeSectionProps";
import { SectionHeader } from "@/features/home/components/shared";
import { statusLabel, statusTone } from "@/features/home/utils/statusPresentation";

export function EventStreamPanel(props: EventStreamPanelProps) {
  return (
    <section className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 shadow-xl shadow-slate-950/20">
      <SectionHeader
        eyebrow="EventStreamPanel"
        title="今日事件流"
        description="点击任一事件卡，唯一去向是同一首页中的主工作区。"
      />
      <div className="mt-4 flex flex-col gap-3">
        {props.eventCards.map((event) => {
          const isActive = event.eventId === props.selectedEventId;
          return (
            <button
              key={event.eventId}
              type="button"
              onClick={() => props.onSelectEvent(event.eventId)}
              className={`rounded-2xl border p-4 text-left transition ${
                isActive
                  ? "border-cyan-400/60 bg-cyan-500/10"
                  : "border-white/10 bg-slate-950/50 hover:border-white/20 hover:bg-white/[0.03]"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <p className="text-sm font-semibold text-white">{event.title}</p>
                <span className={`rounded-full px-2.5 py-1 text-xs ${statusTone(event.processStatus)}`}>
                  {statusLabel(event.processStatus)}
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-300">
                {event.subject} · {event.occurredAt}
              </p>
              <div className="mt-3 flex flex-wrap gap-2 text-xs">
                <span className="rounded-full bg-white/5 px-2.5 py-1 text-slate-300">{event.holdingRelation}</span>
                <span className="rounded-full bg-fuchsia-500/10 px-2.5 py-1 text-fuchsia-200">{event.disclosureFlag}</span>
                <span className="rounded-full bg-cyan-500/10 px-2.5 py-1 text-cyan-100">{event.sourceCard}</span>
              </div>
            </button>
          );
        })}
      </div>
    </section>
  );
}
