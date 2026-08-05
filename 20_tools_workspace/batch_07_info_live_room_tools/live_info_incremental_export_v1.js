(async function () {
  const RUNNER_VERSION = "live_info_incremental_export_v1.1";
  const CHECKPOINT_PREFIX = "__infoLiveIncrementalCheckpointV1__";
  const runtimeOptions = window.__infoLiveIncrementalExportV1Options || {};
  const ROOM_SPEAKER_ALIAS_MAP = {
    "至尊宝": "孙悟空金牌",
    "陈子瞻": "龙头交易猿",
  };

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function normalizeText(text) {
    return String(text || "")
      .replace(/\s+/g, " ")
      .replace(/\u00a0/g, " ")
      .trim();
  }

  function normalizeDateText(text) {
    const raw = normalizeText(text);
    if (!raw) return "";
    const m = raw.match(/(\d{4})[\/-](\d{1,2})[\/-](\d{1,2})/);
    if (!m) return raw;
    const yyyy = m[1];
    const mm = String(m[2]).padStart(2, "0");
    const dd = String(m[3]).padStart(2, "0");
    return `${yyyy}/${mm}/${dd}`;
  }

  function normalizeRoomAnchor(text) {
    return normalizeText(text).replace(/[\\/:*?"<>|]+/g, "_").slice(0, 80) || "unknown_room";
  }

  function isWeakRoomAnchor(text) {
    const value = normalizeText(text);
    if (!value) return true;
    return (
      /^20\d{2}[\/-]\d{1,2}[\/-]\d{1,2}(?:\s+\d{2}:\d{2}(?::\d{2})?)?$/.test(value) ||
      /^\d{2}:\d{2}(?::\d{2})?$/.test(value) ||
      value.length > 30 ||
      /[！!？?￥%]/.test(value) ||
      /^直播间列表\b/i.test(value) ||
      /^搜索直播间名称$/i.test(value) ||
      /^历史记录$/i.test(value) ||
      /^倒序观看$/.test(value) ||
      /^正序观看$/.test(value) ||
      /^V:\d+(?:\.\d+)*/i.test(value) ||
      /搜索直播间名称|直播间列表|历史记录|选择日期|倒序观看|正序观看/.test(value) ||
      /^信息直播间$/i.test(value) ||
      /^MX技术小筑$/i.test(value) ||
      /^(未知|未知房间|unknown_room|unnamed|undefined|null)$/i.test(value)
    );
  }

  function extractLeadingName(text) {
    const value = normalizeText(text)
      .replace(/^讲师\s*/g, "")
      .replace(/^老师\s*/g, "")
      .replace(/^讲师[:：]\s*/g, "")
      .replace(/^老师[:：]\s*/g, "");
    if (!value) return "";
    for (const alias of Object.keys(ROOM_SPEAKER_ALIAS_MAP)) {
      if (value === alias || value.startsWith(alias)) return alias;
    }
    const m = value.match(/^([\u4e00-\u9fa5A-Za-z0-9（）()·\-_]{2,8})(?=$|[：:\s，,。！!？?])/);
    return m ? normalizeText(m[1]) : "";
  }

  function inferRoomAnchorBySpeakerAlias(_initialRoomAnchor, visibleMessages) {
    const freq = {};
    for (const item of visibleMessages || []) {
      const name = item && item.text ? extractLeadingName(item.text) : "";
      if (!name) continue;
      freq[name] = (freq[name] || 0) + 1;
    }
    const top = Object.entries(freq).sort((a, b) => b[1] - a[1])[0];
    if (!top) return "";
    const [name, count] = top;
    if (count < 1) return "";
    const mapped = ROOM_SPEAKER_ALIAS_MAP[name];
    return mapped && !isWeakRoomAnchor(mapped) ? mapped : "";
  }

  function messageKey(roomAnchor, item) {
    return [
      normalizeRoomAnchor(roomAnchor),
      normalizeDateText(item.display_date),
      item.display_time || "",
      normalizeText(item.text).slice(0, 160),
    ].join("||");
  }

  function downloadJson(filename, data) {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function getScrollContainerCandidates() {
    const leftMin = 360;
    const heightMin = 360;
    const result = [];
    const seen = new Set();

    const uniCandidates = Array.from(document.querySelectorAll("uni-scroll-view, .uni-scroll-view, [scroll-y='true']"))
      .filter((el) => el instanceof HTMLElement)
      .map((el) => ({ el, rect: el.getBoundingClientRect() }))
      .filter(({ rect }) => rect.width > 320 && rect.height > heightMin && rect.left > leftMin);
    for (const item of uniCandidates) {
      const className = normalizeText(item.el.className || "");
      const overflowY = window.getComputedStyle(item.el).overflowY || "";
      const scrollableByStyle = /(auto|scroll|overlay)/i.test(overflowY);
      const overflow = (item.el.scrollHeight || 0) - (item.el.clientHeight || 0);
      const isUni = /uni-scroll-view/i.test(item.el.tagName) || /uni-scroll-view/i.test(className);
      let score = 0;
      if (isUni) score += 50000;
      if (scrollableByStyle) score += 20000;
      if (overflow > 40) score += overflow;
      score += Math.min(item.rect.height, 2000);
      if (score > 0 && !seen.has(item.el)) {
        seen.add(item.el);
        result.push({ el: item.el, rect: item.rect, score, overflow });
      }
    }

    const alignedContentRoot = (() => {
      try {
        const last = window.__infoLiveCurrentPageExportV1 || null;
        const probe = last || (typeof window.__runInfoLiveCurrentPageExportV1 === "function" ? window.__runInfoLiveCurrentPageExportV1({ download: false }) : null);
        if (probe && probe.heuristics && probe.heuristics.content_root_pick && probe.heuristics.content_root_pick.picked) {
          const tag = (probe.heuristics.content_root_pick.picked.tag || "").toLowerCase();
          const className = probe.heuristics.content_root_pick.picked.class_name || "";
          const rect = probe.heuristics.content_root_pick.picked.rect || null;
          const guess = Array.from(document.querySelectorAll(tag || "*"))
            .filter((el) => el instanceof HTMLElement)
            .filter((el) => !className || normalizeText(el.className || "") === className)
            .map((el) => ({ el, rect: el.getBoundingClientRect() }))
            .filter(({ rect: r }) => r.left > leftMin && r.height > heightMin && r.width > 320);
          if (guess[0]) return guess[0].el;
        }
      } catch (e) {}
      return null;
    })();

    function pushAncestorScrolls(root) {
      if (!root) return;
      let current = root;
      let depth = 0;
      while (current && current !== document.body && depth < 18) {
        if (current instanceof HTMLElement && !seen.has(current)) {
          const rect = current.getBoundingClientRect();
          if (rect.left > leftMin && rect.width > 320 && rect.height > heightMin) {
            const className = normalizeText(current.className || "");
            const overflowY = window.getComputedStyle(current).overflowY || "";
            const scrollableByStyle = /(auto|scroll|overlay)/i.test(overflowY);
            const overflow = (current.scrollHeight || 0) - (current.clientHeight || 0);
            const isUni = /uni-scroll-view/i.test(current.tagName) || /uni-scroll-view/i.test(className);
            let score = 0;
            if (isUni) score += 50000;
            if (scrollableByStyle) score += 20000;
            if (overflow > 40) score += overflow;
            score += Math.min(rect.height, 2000);
            if (score > 0) {
              seen.add(current);
              result.push({ el: current, rect, score, overflow });
            }
          }
        }
        current = current.parentElement;
        depth += 1;
      }
    }
    pushAncestorScrolls(alignedContentRoot);

    const all = Array.from(document.querySelectorAll("*"))
      .filter((el) => el instanceof HTMLElement)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.width <= 320 || rect.height <= heightMin || rect.left <= leftMin) return null;
        const className = normalizeText(el.className || "");
        const overflowY = window.getComputedStyle(el).overflowY || "";
        const scrollableByStyle = /(auto|scroll|overlay)/i.test(overflowY);
        const overflow = (el.scrollHeight || 0) - (el.clientHeight || 0);
        const isUni = /uni-scroll-view/i.test(el.tagName) || /uni-scroll-view/i.test(className);
        if (overflow <= 40 && !isUni && !scrollableByStyle) return null;
        let score = 0;
        if (isUni) score += 50000;
        if (scrollableByStyle) score += 20000;
        if (overflow > 40) score += overflow;
        score += Math.min(rect.height, 2000);
        return { el, rect, score, overflow };
      })
      .filter(Boolean);
    for (const item of all) {
      if (!seen.has(item.el)) {
        seen.add(item.el);
        result.push(item);
      }
    }

    result.sort((a, b) => b.score - a.score);
    return result;
  }

  function testScrollContainer(el) {
    try {
      if (!(el instanceof HTMLElement)) return false;
      const maxTop = Math.max(0, (el.scrollHeight || 0) - (el.clientHeight || 0));
      if (maxTop <= 20) return false;
      const original = el.scrollTop;
      const probe1 = Math.max(0, Math.min(maxTop, Math.floor(maxTop / 2)));
      el.scrollTop = probe1;
      const ok1 = Math.abs(el.scrollTop - probe1) < 8 || Math.abs(el.scrollTop - original) >= 8;
      const probe2 = Math.max(0, Math.min(maxTop, original + 8));
      el.scrollTop = probe2;
      const ok2 = Math.abs(el.scrollTop - probe2) < 8 || Math.abs(el.scrollTop - probe1) >= 4;
      el.scrollTop = original;
      return ok1 || ok2;
    } catch (e) {
      return false;
    }
  }

  function getScrollContainer() {
    const ranked = getScrollContainerCandidates();
    const tested = [];
    for (const item of ranked.slice(0, 8)) {
      const ok = testScrollContainer(item.el);
      tested.push({ el: item.el, tag: item.el.tagName, score: item.score, ok });
      if (ok) return item.el;
    }
    console.warn("[增量] 没有通过 scroll-set 自测的容器，回退取分数最高者", tested);
    return ranked[0]?.el || null;
  }

  function detectNoMoreRecordsText() {
    const keywords = ["没有更多记录", "没有更多记录了", "暂无更多记录"];
    const nodes = Array.from(document.querySelectorAll("body *"))
      .filter((el) => el instanceof HTMLElement)
      .slice(0, 4000);
    for (const el of nodes) {
      const rect = el.getBoundingClientRect();
      if (rect.width <= 120 || rect.height <= 16) continue;
      if (rect.left <= 350) continue;
      const text = normalizeText(el.innerText || el.textContent || "");
      if (!text) continue;
      for (const kw of keywords) {
        if (text.includes(kw)) return true;
      }
    }
    return false;
  }

  async function waitForStableViewport(runnerState) {
    let stableCount = 0;
    let lastSignature = "";
    const maxIters = Number(runtimeOptions.stable_iters || runtimeOptions.stableIters || 10);
    const iterSleep = Number(runtimeOptions.stable_sleep_ms || runtimeOptions.stableSleepMs || 120);

    for (let i = 0; i < maxIters; i += 1) {
      await sleep(iterSleep);
      const result = window.__runInfoLiveCurrentPageExportV1({ download: false });
      const signature = (result.visible_messages || [])
        .slice(0, 3)
        .map((item) => `${normalizeDateText(item.display_date)} ${item.display_time || ""} ${normalizeText(item.text).slice(0, 20)}`)
        .join(" | ");

      if (signature && signature === lastSignature) {
        stableCount += 1;
      } else {
        stableCount = 0;
      }
      lastSignature = signature;

      runnerState.lastPreview = result;
      const msgCount = (result.visible_messages || []).length;
      if (stableCount >= 1) return result;
      if (signature && msgCount > 0 && i >= 3) return result;
      if (!signature && msgCount === 0 && i >= Math.min(5, maxIters - 1)) return result;
    }

    return runnerState.lastPreview || window.__runInfoLiveCurrentPageExportV1({ download: false });
  }

  function mergeMessages(roomAnchor, bucket, visibleMessages) {
    let added = 0;
    for (const item of visibleMessages || []) {
      const normalizedItem = {
        ...item,
        display_date: normalizeDateText(item.display_date),
      };
      const key = messageKey(roomAnchor, normalizedItem);
      if (!bucket.map[key]) {
        bucket.map[key] = {
          ...normalizedItem,
          dedup_key: key,
        };
        bucket.list.push(bucket.map[key]);
        added += 1;
      }
    }
    bucket.list.sort((a, b) => {
      const left = `${normalizeDateText(a.display_date)} ${a.display_time || ""}`;
      const right = `${normalizeDateText(b.display_date)} ${b.display_time || ""}`;
      if (left < right) return -1;
      if (left > right) return 1;
      return normalizeText(a.text).localeCompare(normalizeText(b.text), "zh-CN");
    });
    return added;
  }

  function buildCheckpointKey(roomAnchor) {
    return `${CHECKPOINT_PREFIX}${normalizeRoomAnchor(roomAnchor)}`;
  }

  function loadCheckpoint(roomAnchor) {
    try {
      const raw = localStorage.getItem(buildCheckpointKey(roomAnchor));
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function saveCheckpoint(roomAnchor, checkpoint) {
    localStorage.setItem(buildCheckpointKey(roomAnchor), JSON.stringify(checkpoint));
  }

  function clearCheckpoint(roomAnchor) {
    localStorage.removeItem(buildCheckpointKey(roomAnchor));
  }

  if (typeof window.__runInfoLiveCurrentPageExportV1 !== "function") {
    throw new Error("请先运行 live_info_current_page_export_v1.js，再运行增量脚本。");
  }

  const container = getScrollContainer();
  if (!container) {
    throw new Error("未找到右侧历史消息滚动容器。");
  }

  const resetCheckpoint = runtimeOptions.reset_checkpoint === true || runtimeOptions.resetCheckpoint === true;
  const startPosition = runtimeOptions.start_position || runtimeOptions.startPosition || "keep";
  const scrollDirection = runtimeOptions.scroll_direction || runtimeOptions.scrollDirection || "down";

  if (resetCheckpoint) {
    if (startPosition === "top") {
      container.scrollTop = 0;
      container.dispatchEvent(new Event("scroll", { bubbles: true }));
      await sleep(500);
    } else if (startPosition === "bottom") {
      container.scrollTop = container.scrollHeight;
      container.dispatchEvent(new Event("scroll", { bubbles: true }));
      await sleep(500);
    }
  }

  const initial = await waitForStableViewport({});
  let roomAnchor = initial.room_anchor || "unknown_room";
  // Prefer speaker alias even when sidebar mis-picks a short wrong room name (e.g. 先知).
  const aliasRoom = inferRoomAnchorBySpeakerAlias(roomAnchor, initial.visible_messages || []);
  if (aliasRoom) {
    roomAnchor = aliasRoom;
  } else if (isWeakRoomAnchor(roomAnchor)) {
    const heur = (initial && initial.heuristics) || {};
    const candidates = [
      heur.initial_room_anchor_candidate,
      heur.room_anchor_candidate,
      heur.topic_anchor_candidate,
    ].filter((x) => x && !isWeakRoomAnchor(x));
    if (candidates[0]) roomAnchor = candidates[0];
  }
  if (resetCheckpoint) {
    clearCheckpoint(roomAnchor);
  }
  const checkpoint = loadCheckpoint(roomAnchor);
  const store = {
    map: {},
    list: [],
  };

  let stopReason = "manual_limit";
  let loopCount = 0;
  let noNewRounds = 0;
  const maxRounds = Number(runtimeOptions.max_rounds || runtimeOptions.maxRounds || 180);
  const maxNoNewRounds = Number(runtimeOptions.max_no_new_rounds || runtimeOptions.maxNoNewRounds || 3);
  const overlapMessages = 3;
  let viewportStep = Math.max(
    380,
    Number(runtimeOptions.viewport_step || runtimeOptions.viewportStep || Math.floor(container.clientHeight * 0.9))
  );
  const scrollSleepMs = Number(runtimeOptions.scroll_sleep_ms || runtimeOptions.scrollSleepMs || 320);
  let newlyAddedCount = 0;
  const startScrollTop = container.scrollTop;
  const checkpointLoadedCount = checkpoint && Array.isArray(checkpoint.messages)
    ? checkpoint.messages.length
    : 0;
  console.log(`[增量启动] room=${roomAnchor} start_scroll=${startScrollTop} step=${viewportStep} max_rounds=${maxRounds}`, {
    container: container.tagName,
    rect: container.getBoundingClientRect(),
    scrollHeight: container.scrollHeight,
    clientHeight: container.clientHeight,
  });

  if (checkpoint && Array.isArray(checkpoint.messages)) {
    for (const item of checkpoint.messages) {
      const normalizedItem = { ...item, display_date: normalizeDateText(item.display_date) };
      const key = messageKey(roomAnchor, normalizedItem);
      store.map[key] = { ...normalizedItem, dedup_key: key };
      store.list.push(store.map[key]);
    }
  }

  if (
    checkpoint &&
    typeof checkpoint.scroll_top === "number" &&
    Number.isFinite(checkpoint.scroll_top) &&
    checkpoint.scroll_top >= 0
  ) {
    container.scrollTop = checkpoint.scroll_top;
    container.dispatchEvent(new Event("scroll", { bubbles: true }));
    await sleep(500);
  }

  let lastScrollTop = container.scrollTop;
  let currentResult = initial;

  while (loopCount < maxRounds) {
    const added = mergeMessages(roomAnchor, store, currentResult.visible_messages || []);
    newlyAddedCount += added;
    noNewRounds = added === 0 ? noNewRounds + 1 : 0;

    const checkpointPayload = {
      runner_version: RUNNER_VERSION,
      room_anchor: roomAnchor,
      page_url: location.href,
      saved_at: new Date().toISOString(),
      scroll_top: container.scrollTop,
      overlap_preview: (currentResult.visible_messages || [])
        .slice(-overlapMessages)
        .map((item) => ({
          display_date: item.display_date,
          display_time: item.display_time,
          text: normalizeText(item.text).slice(0, 80),
        })),
      message_count: store.list.length,
      messages: store.list,
    };
    saveCheckpoint(roomAnchor, checkpointPayload);

    const rangeFirst = store.list[0];
    const rangeLast = store.list[store.list.length - 1];
    console.log(
      `[增量 round=${loopCount}] +${added} 累计=${store.list.length} 无新=${noNewRounds}/${maxNoNewRounds} scroll=${container.scrollTop}/${Math.max(0, container.scrollHeight - container.clientHeight)} 采样=${(rangeFirst?.display_time || "")}..${(rangeLast?.display_time || "")}`
    );

    if (noNewRounds >= maxNoNewRounds) {
      stopReason = "no_new_messages";
      break;
    }

    const maxScrollTop = Math.max(0, container.scrollHeight - container.clientHeight);
    if (maxScrollTop <= 1) {
      stopReason = "not_scrollable";
      break;
    }

    const directionSign = scrollDirection === "up" ? -1 : 1;
    let proposed = container.scrollTop + directionSign * viewportStep;
    let nextScrollTop = Math.min(maxScrollTop, Math.max(0, proposed));
    if (nextScrollTop === container.scrollTop) {
      const boostedStep = viewportStep * 2;
      proposed = container.scrollTop + directionSign * boostedStep;
      nextScrollTop = Math.min(maxScrollTop, Math.max(0, proposed));
      if (nextScrollTop !== container.scrollTop) {
        console.log(`[增量] 原步长卡住，放大步长到 ${boostedStep} 再推一次`);
      }
    }
    if (nextScrollTop === container.scrollTop) {
      stopReason = "scroll_end";
      break;
    }

    container.scrollTop = nextScrollTop;
    container.dispatchEvent(new Event("scroll", { bubbles: true }));
    await sleep(scrollSleepMs);
    currentResult = await waitForStableViewport({});

    if (container.scrollTop === lastScrollTop) {
      const eps = 80;
      const noMore = detectNoMoreRecordsText();
      if (scrollDirection === "up") {
        if (container.scrollTop <= eps || noMore) {
          stopReason = "scroll_end";
          break;
        }
      } else {
        if (container.scrollTop >= maxScrollTop - eps || noMore) {
          stopReason = "scroll_end";
          break;
        }
      }
      stopReason = "scroll_stuck";
      break;
    }
    lastScrollTop = container.scrollTop;
    loopCount += 1;
  }

  const exportTs = new Date().toISOString();
  const fileTs = exportTs
    .replace(/[-:]/g, "")
    .replace(/\..+/, "")
    .replace("T", "_");

  const finalResult = {
    export_version: RUNNER_VERSION,
    exported_at: exportTs,
    room_anchor: roomAnchor,
    page_url: location.href,
    source_family: "信息直播间",
    access_mode: "login_state_required",
    checkpoint_key: buildCheckpointKey(roomAnchor),
    stop_reason: stopReason,
    rounds_completed: loopCount,
    message_count: store.list.length,
    resumed_from_checkpoint: Boolean(checkpoint),
    checkpoint_loaded_count: checkpointLoadedCount,
    newly_added_count: newlyAddedCount,
    start_scroll_top: startScrollTop,
    end_scroll_top: container.scrollTop,
    runtime_options: {
      reset_checkpoint: runtimeOptions.reset_checkpoint === true || runtimeOptions.resetCheckpoint === true,
      max_rounds: maxRounds,
      max_no_new_rounds: maxNoNewRounds,
      viewport_step: viewportStep,
    },
    sample_range: {
      first: store.list[0] || null,
      last: store.list[store.list.length - 1] || null,
    },
    messages: store.list,
  };

  const filename = `info_live_incremental_export__${fileTs}.json`;
  window.__infoLiveIncrementalExportV1 = finalResult;
  downloadJson(filename, finalResult);
  console.log(RUNNER_VERSION, finalResult);
  return finalResult;
})();
