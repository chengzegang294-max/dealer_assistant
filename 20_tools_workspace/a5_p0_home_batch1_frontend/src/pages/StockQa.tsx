import { useStockQaPage } from "@/features/stock/hooks/useStockQaPage";

export default function StockQa() {
  const {
    stockCode,
    stockName,
    selectedEventTitle,
    selectedEventSubject,
    hasLoaded,
    recommendedQuestions,
    selectedQuestion,
    answerBlocks,
    latestRecord,
    stillNeedEvidenceLabel,
    setSelectedQuestion,
    handleBackStock,
  } = useStockQaPage();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-5xl flex-col gap-6 px-4 py-6 lg:px-6">
        <header className="rounded-3xl border border-white/10 bg-slate-900/80 p-6 shadow-2xl shadow-slate-950/30">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="space-y-3">
              <p className="text-xs uppercase tracking-[0.35em] text-cyan-300/80">Batch2 QA Placeholder</p>
              <div>
                <h1 className="text-3xl font-semibold text-white">
                  {stockName}
                  <span className="ml-3 text-lg text-slate-400">{stockCode}</span>
                </h1>
                <p className="mt-2 text-sm text-slate-300">
                  当前是问答下钻占位页，只做有上下文的解释增强，不做自由聊天或价格预测。
                </p>
              </div>
              <div className="flex flex-wrap gap-2 text-xs text-slate-200">
                <span className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1">
                  当前事件：{selectedEventTitle}
                </span>
                <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1">
                  对象：{selectedEventSubject}
                </span>
                <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1">
                  {stillNeedEvidenceLabel}
                </span>
              </div>
            </div>

            <button
              type="button"
              onClick={handleBackStock}
              className="rounded-xl border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:border-cyan-400/40 hover:text-white"
            >
              回到标的页
            </button>
          </div>
        </header>

        {!hasLoaded ? (
          <section className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 text-sm text-slate-300">
            正在加载问答上下文...
          </section>
        ) : (
          <main className="grid gap-6 xl:grid-cols-[0.9fr_1.2fr]">
            <section className="rounded-3xl border border-white/10 bg-slate-900/60 p-5">
              <div className="mb-4">
                <p className="text-xs uppercase tracking-[0.3em] text-cyan-300/70">推荐问题区</p>
                <h2 className="mt-2 text-xl font-semibold text-white">围绕当前事件，只问这几类</h2>
              </div>
              <div className="space-y-3">
                {recommendedQuestions.map((question) => (
                  <button
                    key={question}
                    type="button"
                    onClick={() => setSelectedQuestion(question)}
                    className={`w-full rounded-2xl border p-4 text-left text-sm transition ${
                      selectedQuestion === question
                        ? "border-cyan-400/50 bg-cyan-400/10 text-cyan-50"
                        : "border-white/10 bg-slate-950/40 text-slate-200 hover:border-white/20"
                    }`}
                  >
                    {question}
                  </button>
                ))}
              </div>

              <div className="mt-6 rounded-2xl border border-white/10 bg-slate-950/40 p-4 text-sm text-slate-300">
                <p className="text-xs uppercase tracking-[0.25em] text-slate-500">最近记录参考</p>
                <p className="mt-2">
                  {latestRecord
                    ? `${latestRecord.action} / ${latestRecord.reasonTag} / ${latestRecord.horizon}`
                    : "当前没有直接绑定记录，回答只回链当前事件字段。"}
                </p>
              </div>
            </section>

            <section className="rounded-3xl border border-white/10 bg-slate-900/60 p-5">
              <div className="mb-4">
                <p className="text-xs uppercase tracking-[0.3em] text-cyan-300/70">问答结果区</p>
                <h2 className="mt-2 text-xl font-semibold text-white">{selectedQuestion ?? "请选择一个推荐问题"}</h2>
                <p className="mt-1 text-sm text-slate-400">
                  当前回答严格遵循：回链事件、补充解释、提醒记录/回看、保留金融限制。
                </p>
              </div>
              <div className="space-y-4">
                {answerBlocks.map((block) => (
                  <div key={block.title} className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
                    <p className="text-xs uppercase tracking-[0.25em] text-slate-500">{block.title}</p>
                    <p className="mt-2 text-sm text-slate-200">{block.content}</p>
                  </div>
                ))}
              </div>
            </section>
          </main>
        )}
      </div>
    </div>
  );
}
