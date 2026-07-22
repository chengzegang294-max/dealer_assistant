import type { HomeSidebarProps } from "@/features/home/contracts/homeSectionProps";
import { SectionHeader } from "@/features/home/components/shared";

export function HomeSidebar(props: HomeSidebarProps) {
  const { viewModel, actions } = props;

  return (
    <aside className="flex flex-col gap-6">
      <section className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 shadow-xl shadow-slate-950/20">
        <SectionHeader
          eyebrow="DecisionQueueSummary"
          title="待处理摘要"
          description="这里只保留未处理事件，点击后重新进入同一主工作区。"
        />
        <div className="mt-4 flex flex-col gap-3">
          {viewModel.queuedEventCards.length ? (
            viewModel.queuedEventCards.map((event) => (
              <button
                key={event.eventId}
                type="button"
                onClick={() => actions.onSelectEvent(event.eventId)}
                className="rounded-2xl border border-white/10 bg-slate-950/40 p-4 text-left transition hover:border-cyan-400/30"
              >
                <p className="text-sm font-medium text-white">{event.title}</p>
                <p className="mt-2 text-xs text-slate-400">{event.subject} · {event.occurredAt}</p>
              </button>
            ))
          ) : (
            <p className="text-sm text-slate-400">{viewModel.queuedEmptyMessage}</p>
          )}
        </div>
      </section>

      <section className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 shadow-xl shadow-slate-950/20">
        <SectionHeader
          eyebrow="HistoryTracePanel"
          title="最近记录区"
          description="这里保留最近的记录结果和最新一次提交回显。"
        />
        <div className="mt-4 flex flex-col gap-3">
          {viewModel.recentRecordCards.map((record) => (
            <article key={record.id} className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
              <p className="text-sm font-medium text-white">{record.title}</p>
              <p className="mt-2 text-xs text-slate-300">{record.summaryLine}</p>
              {record.note ? <p className="mt-2 text-sm text-slate-400">{record.note}</p> : null}
              <p className="mt-2 text-xs text-slate-500">{record.submittedAt}</p>
            </article>
          ))}
        </div>
      </section>

      <section
        id="finance-disclosure-note"
        className="rounded-3xl border border-fuchsia-400/20 bg-fuchsia-500/10 p-5 shadow-xl shadow-slate-950/20"
      >
        <p className="text-xs font-medium uppercase tracking-[0.22em] text-fuchsia-200">金融限制短披露层</p>
        <p className="mt-3 text-sm text-fuchsia-50">{viewModel.financeDisclosureDetail}</p>
        <p className="mt-2 text-xs text-fuchsia-100/80">
          所有事件卡都固定展示 `{viewModel.financeDisclosureLabel}`，当前说明不升格成确定性结论。
        </p>
      </section>
    </aside>
  );
}
