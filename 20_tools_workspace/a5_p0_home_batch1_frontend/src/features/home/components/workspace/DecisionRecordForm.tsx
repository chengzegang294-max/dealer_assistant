import type { DecisionRecordFormViewModel } from "@/features/home/adapters/homeViewModel";
import { FormSelect } from "@/features/home/components/shared";
import {
  type DecisionAction,
  type DecisionDraft,
  type DecisionDraftChangeHandler,
  type Horizon,
  type ReasonTag,
} from "@/features/home/types";

interface DecisionRecordFormProps {
  viewModel: DecisionRecordFormViewModel;
  homeRecordDraft: DecisionDraft;
  formError: string | null;
  onChangeDecisionDraft: DecisionDraftChangeHandler;
  onSubmitDecision: () => void;
  onRetrySubmitDecision: () => void;
}

export function DecisionRecordForm(props: DecisionRecordFormProps) {
  const { viewModel, homeRecordDraft, formError, onChangeDecisionDraft, onSubmitDecision, onRetrySubmitDecision } = props;

  return (
    <article className="rounded-3xl border border-white/10 bg-slate-950/40 p-5">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.22em] text-slate-400">{viewModel.eyebrow}</p>
          <p className="mt-2 text-sm text-slate-300">{viewModel.description}</p>
        </div>
        <span className="rounded-full bg-white/5 px-3 py-1 text-xs text-slate-300">{viewModel.draftEventLabel}</span>
      </div>

      <div className="mt-4 grid gap-4 md:grid-cols-3">
        <FormSelect
          label={viewModel.actionField.label}
          value={homeRecordDraft.action}
          placeholder={viewModel.actionField.placeholder}
          options={viewModel.actionField.options}
          onChange={(value) => onChangeDecisionDraft("action", value as DecisionAction)}
        />
        <FormSelect
          label={viewModel.reasonTagField.label}
          value={homeRecordDraft.reasonTag}
          placeholder={viewModel.reasonTagField.placeholder}
          options={viewModel.reasonTagField.options}
          onChange={(value) => onChangeDecisionDraft("reasonTag", value as ReasonTag)}
        />
        <FormSelect
          label={viewModel.horizonField.label}
          value={homeRecordDraft.horizon}
          placeholder={viewModel.horizonField.placeholder}
          options={viewModel.horizonField.options}
          onChange={(value) => onChangeDecisionDraft("horizon", value as Horizon)}
        />
      </div>

      <label className="mt-4 block">
        <span className="mb-2 block text-sm font-medium text-slate-200">{viewModel.noteLabel}</span>
        <textarea
          value={homeRecordDraft.note}
          onChange={(event) => onChangeDecisionDraft("note", event.target.value)}
          rows={4}
          placeholder={viewModel.notePlaceholder}
          className="w-full rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-400/50"
        />
      </label>

      {formError ? <p className="mt-3 text-sm text-rose-300">{formError}</p> : null}

      <div className="mt-4 flex flex-wrap gap-3">
        <button
          type="button"
          onClick={onSubmitDecision}
          className="rounded-2xl bg-emerald-400 px-4 py-3 text-sm font-medium text-slate-950 transition hover:bg-emerald-300"
        >
          {viewModel.submitButtonLabel}
        </button>
        <button
          type="button"
          onClick={onRetrySubmitDecision}
          className="rounded-2xl border border-white/10 px-4 py-3 text-sm font-medium text-slate-200 transition hover:border-white/20 hover:text-white"
        >
          {viewModel.retryButtonLabel}
        </button>
      </div>
    </article>
  );
}
