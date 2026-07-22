import type { SubmitEcho } from "@/features/home/types";

interface SubmitEchoPanelProps {
  latestSubmitEcho: SubmitEcho | null;
}

export function SubmitEchoPanel(props: SubmitEchoPanelProps) {
  return (
    <article className="rounded-3xl border border-white/10 bg-slate-950/40 p-5">
      <p className="text-xs font-medium uppercase tracking-[0.22em] text-slate-400">提交回显</p>
      {props.latestSubmitEcho ? (
        <div className="mt-3 rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-4">
          <p className="text-sm font-medium text-emerald-100">{props.latestSubmitEcho.title}</p>
          <p className="mt-2 text-sm text-emerald-50/90">{props.latestSubmitEcho.summary}</p>
          <p className="mt-2 text-xs text-emerald-100/80">提交时间：{props.latestSubmitEcho.submittedAt}</p>
        </div>
      ) : (
        <p className="mt-3 text-sm text-slate-400">当前还没有最新提交回显。切事件时这里会被主动清空，避免旧事件污染新事件。</p>
      )}
    </article>
  );
}
