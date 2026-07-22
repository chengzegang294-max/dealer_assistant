import { useStockPage } from "@/features/stock/hooks/useStockPage";

export default function Stock() {
  const {
    stockCode,
    hasLoaded,
    headerViewModel,
    relatedEventsViewModel,
    explanationViewModel,
    recentRecordViewModel,
    qaEntryViewModel,
    canSupplementRecord,
    isSupplementEditorOpen,
    supplementDraft,
    supplementError,
    latestSupplementEcho,
    setSupplementDraft,
    handleSelectEvent,
    handleOpenSupplementEditor,
    handleSubmitSupplement,
    handleBackHome,
  } = useStockPage();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-6 px-4 py-6 lg:px-6">
        <header className="rounded-3xl border border-white/10 bg-slate-900/80 p-6 shadow-2xl shadow-slate-950/30">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="space-y-3">
              <p className="text-xs uppercase tracking-[0.35em] text-cyan-300/80">Batch2 Stock Shell</p>
              <div>
                <h1 className="text-3xl font-semibold text-white">
                  {headerViewModel.stockName}
                  <span className="ml-3 text-lg text-slate-400">{headerViewModel.stockCode}</span>
                </h1>
                <p className="mt-2 text-sm text-slate-300">
                  当前角色：标的分析页最小壳。只回答最近发生了什么、为什么触发、之前怎么处理过、还能问什么。
                </p>
              </div>
              <div className="flex flex-wrap gap-2 text-xs text-slate-200">
                <span className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1">
                  关系：{headerViewModel.holdingRelationLabel}
                </span>
                <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1">
                  最近状态：{headerViewModel.latestEventStatusLabel}
                </span>
                <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-3 py-1">
                  still_need_evidence
                </span>
              </div>
              <div className="flex flex-wrap gap-2 text-xs text-slate-400">
                {headerViewModel.sourceTags.map((tag) => (
                  <span key={tag} className="rounded-full border border-white/10 px-3 py-1">
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            <button
              type="button"
              onClick={handleBackHome}
              className="rounded-xl border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:border-cyan-400/40 hover:text-white"
            >
              返回首页事件流
            </button>
          </div>
        </header>

        {!hasLoaded ? (
          <section className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 text-sm text-slate-300">
            正在加载 {stockCode} 的最小上下文...
          </section>
        ) : (
          <main className="grid gap-6 xl:grid-cols-[0.95fr_1.3fr]">
            <section className="rounded-3xl border border-white/10 bg-slate-900/60 p-5">
              <div className="mb-4">
                <p className="text-xs uppercase tracking-[0.3em] text-cyan-300/70">相关事件区</p>
                <h2 className="mt-2 text-xl font-semibold text-white">先看这只标的最近发生了什么</h2>
              </div>
              <div className="space-y-3">
                {relatedEventsViewModel.map((event) => (
                  <button
                    key={event.eventId}
                    type="button"
                    onClick={() => handleSelectEvent(event.eventId)}
                    className={`w-full rounded-2xl border p-4 text-left transition ${
                      event.isSelected
                        ? "border-cyan-400/50 bg-cyan-400/10"
                        : "border-white/10 bg-slate-950/40 hover:border-white/20"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h3 className="text-sm font-medium text-white">{event.title}</h3>
                        <p className="mt-1 text-xs text-slate-400">{event.category}</p>
                      </div>
                      <span className="text-xs text-slate-400">{event.occurredAt}</span>
                    </div>
                    <p className="mt-3 text-xs text-slate-300">{event.processStatusLabel}</p>
                  </button>
                ))}
              </div>
            </section>

            <div className="flex flex-col gap-6">
              <section className="rounded-3xl border border-white/10 bg-slate-900/60 p-5">
                <div className="mb-4">
                  <p className="text-xs uppercase tracking-[0.3em] text-cyan-300/70">当前解释区</p>
                  <h2 className="mt-2 text-xl font-semibold text-white">
                    {explanationViewModel?.title ?? "当前还没有可展示的解释"}
                  </h2>
                  <p className="mt-1 text-sm text-slate-400">{explanationViewModel?.subject ?? "请选择相关事件"}</p>
                </div>
                {explanationViewModel ? (
                  <div className="space-y-4 text-sm text-slate-200">
                    <div>
                      <p className="text-xs uppercase tracking-[0.25em] text-slate-500">触发逻辑</p>
                      <p className="mt-2 text-slate-200">{explanationViewModel.logic}</p>
                    </div>
                    <div>
                      <p className="text-xs uppercase tracking-[0.25em] text-slate-500">影响推演</p>
                      <p className="mt-2 text-slate-200">{explanationViewModel.impact}</p>
                    </div>
                    <div>
                      <p className="text-xs uppercase tracking-[0.25em] text-slate-500">历史类比</p>
                      <p className="mt-2 text-slate-200">{explanationViewModel.historyAnalogy}</p>
                    </div>
                    <div>
                      <p className="text-xs uppercase tracking-[0.25em] text-slate-500">下一次复查点</p>
                      <p className="mt-2 text-slate-200">{explanationViewModel.nextReviewPoint}</p>
                    </div>
                  </div>
                ) : (
                  <p className="text-sm text-slate-400">Batch2 只保留最小上下文，不扩成自由分析页。</p>
                )}
              </section>

              <section className="rounded-3xl border border-white/10 bg-slate-900/60 p-5">
                <div className="mb-4">
                  <p className="text-xs uppercase tracking-[0.3em] text-cyan-300/70">最近决策记录区</p>
                  <h2 className="mt-2 text-xl font-semibold text-white">最近怎么处理过</h2>
                </div>
                {recentRecordViewModel ? (
                  <div className="grid gap-3 text-sm text-slate-200 md:grid-cols-2">
                    <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
                      <p className="text-xs uppercase tracking-[0.25em] text-slate-500">最近动作</p>
                      <p className="mt-2">{recentRecordViewModel.action}</p>
                      <p className="mt-3 text-xs text-slate-400">{recentRecordViewModel.statusLabel}</p>
                    </div>
                    <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-4">
                      <p className="text-xs uppercase tracking-[0.25em] text-slate-500">理由标签 / 周期</p>
                      <p className="mt-2">
                        {recentRecordViewModel.reasonTag} / {recentRecordViewModel.horizon}
                      </p>
                    </div>
                    <div className="rounded-2xl border border-white/10 bg-slate-950/40 p-4 md:col-span-2">
                      <p className="text-xs uppercase tracking-[0.25em] text-slate-500">备注</p>
                      <p className="mt-2">{recentRecordViewModel.note}</p>
                      <p className="mt-3 text-xs text-slate-400">{recentRecordViewModel.submittedAt}</p>
                    </div>
                    <div className="rounded-2xl border border-cyan-400/20 bg-cyan-400/5 p-4 md:col-span-2">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <p className="text-xs uppercase tracking-[0.25em] text-cyan-300/70">补充记录入口区</p>
                          <p className="mt-2 text-sm text-slate-300">
                            当前事件已锁定时，可直接补充备注，不改原动作、理由标签和周期。
                          </p>
                        </div>
                        <button
                          type="button"
                          onClick={handleOpenSupplementEditor}
                          disabled={!canSupplementRecord}
                          className={`rounded-xl px-4 py-2 text-sm transition ${
                            canSupplementRecord
                              ? "border border-cyan-400/40 bg-cyan-400/10 text-cyan-100 hover:bg-cyan-400/20"
                              : "cursor-not-allowed border border-white/10 text-slate-500"
                          }`}
                        >
                          补充这次记录
                        </button>
                      </div>

                      {isSupplementEditorOpen ? (
                        <div className="mt-4 rounded-2xl border border-white/10 bg-slate-950/40 p-4">
                          <p className="text-xs uppercase tracking-[0.25em] text-slate-500">当前上下文</p>
                          <p className="mt-2 text-sm text-slate-200">
                            {headerViewModel.stockName} / {explanationViewModel?.title ?? "当前事件"}
                          </p>
                          <textarea
                            value={supplementDraft}
                            onChange={(event) => setSupplementDraft(event.target.value)}
                            placeholder="补充这次记录的原因、变化或下一步观察点"
                            className="mt-4 min-h-28 w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 text-sm text-slate-100 outline-none"
                          />
                          {supplementError ? <p className="mt-3 text-sm text-rose-300">{supplementError}</p> : null}
                          <div className="mt-4 flex justify-end">
                            <button
                              type="button"
                              onClick={handleSubmitSupplement}
                              className="rounded-xl border border-cyan-400/40 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-100 transition hover:bg-cyan-400/20"
                            >
                              提交补充备注
                            </button>
                          </div>
                        </div>
                      ) : null}

                      {latestSupplementEcho ? (
                        <div className="mt-4 rounded-2xl border border-emerald-400/20 bg-emerald-400/10 p-4">
                          <p className="text-xs uppercase tracking-[0.25em] text-emerald-200/80">最近一次补充回显区</p>
                          <p className="mt-2 text-sm text-emerald-50">{latestSupplementEcho.note}</p>
                          <p className="mt-3 text-xs text-emerald-100/70">{latestSupplementEcho.submittedAt}</p>
                        </div>
                      ) : null}
                    </div>
                  </div>
                ) : (
                  <div className="rounded-2xl border border-dashed border-white/10 bg-slate-950/30 p-4 text-sm text-slate-400">
                    当前还没有与该事件直接绑定的最近记录。Batch2 先落区块与空态，不继续推进补充记录编辑流。
                  </div>
                )}
              </section>

              <section className="rounded-3xl border border-white/10 bg-slate-900/60 p-5">
                <div className="mb-4">
                  <p className="text-xs uppercase tracking-[0.3em] text-cyan-300/70">问答下钻入口区</p>
                  <h2 className="mt-2 text-xl font-semibold text-white">还能问什么</h2>
                  <p className="mt-1 text-sm text-slate-400">
                    当前只保留下钻入口位，不在本轮实现问答页本体。
                  </p>
                </div>
                <div className="mb-4 rounded-2xl border border-white/10 bg-slate-950/40 p-4">
                  <label className="mb-2 block text-xs uppercase tracking-[0.25em] text-slate-500">
                    问答输入占位
                  </label>
                  <input
                    type="text"
                    disabled
                    placeholder="输入你想追问的问题（后续批次开启）"
                    className="w-full cursor-not-allowed rounded-xl border border-white/10 bg-slate-950/70 px-4 py-3 text-sm text-slate-500 outline-none"
                  />
                </div>
                <div className="grid gap-3 md:grid-cols-2">
                  {qaEntryViewModel.questions.map((question) => (
                    <div key={question} className="rounded-2xl border border-white/10 bg-slate-950/40 p-4 text-sm text-slate-200">
                      {question}
                    </div>
                  ))}
                </div>
                <div className="mt-4 flex items-center justify-between gap-3 rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4">
                  <p className="text-sm text-amber-100">
                    当前限制：{qaEntryViewModel.stillNeedEvidenceLabel}。不输出自由荐股或价格预测。
                  </p>
                  <button
                    type="button"
                    disabled
                    className="cursor-not-allowed rounded-xl border border-white/10 px-4 py-2 text-sm text-slate-400"
                  >
                    问答下钻（后续批次）
                  </button>
                </div>
              </section>
            </div>
          </main>
        )}
      </div>
    </div>
  );
}
