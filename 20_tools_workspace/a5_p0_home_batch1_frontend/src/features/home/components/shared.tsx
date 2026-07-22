export function SectionHeader(props: { eyebrow: string; title: string; description: string }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-[0.22em] text-slate-400">{props.eyebrow}</p>
      <h2 className="mt-2 text-xl font-semibold text-white">{props.title}</h2>
      <p className="mt-2 text-sm text-slate-400">{props.description}</p>
    </div>
  );
}

export function StatusMetric(props: { title: string; value: string; hint: string }) {
  return (
    <article className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
      <p className="text-xs font-medium uppercase tracking-[0.22em] text-slate-400">{props.title}</p>
      <p className="mt-3 text-sm font-medium text-white">{props.value}</p>
      <p className="mt-2 text-xs text-slate-500">{props.hint}</p>
    </article>
  );
}

export function InfoBlock(props: { title: string; content: string }) {
  return (
    <article className="rounded-2xl border border-white/10 bg-white/[0.02] p-4">
      <p className="text-xs font-medium uppercase tracking-[0.22em] text-slate-400">{props.title}</p>
      <p className="mt-3 text-sm text-slate-200">{props.content}</p>
    </article>
  );
}

export function FormSelect(props: {
  label: string;
  value: string;
  placeholder: string;
  options: string[];
  onChange: (value: string) => void;
}) {
  return (
    <label>
      <span className="mb-2 block text-sm font-medium text-slate-200">{props.label}</span>
      <select
        value={props.value}
        onChange={(event) => props.onChange(event.target.value)}
        className="w-full rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-400/50"
      >
        <option value="">{props.placeholder}</option>
        {props.options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}
