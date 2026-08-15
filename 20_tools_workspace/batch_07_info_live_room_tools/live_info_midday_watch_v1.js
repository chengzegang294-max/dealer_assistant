/**
 * live_info_midday_watch_v1
 *
 * 盘中「列表哨兵」v0：停在信息直播间主页（能见左侧房列表）时粘贴一次。
 * 定时扫 A+B 优先房的「标题 + 预览 + 时间」指纹，变化则 Console 告警。
 *
 * 能做到：
 * - 盯 A/B 谁更新了（列表预览变了）
 * - 可选只盯 A / 自定义名单
 * - 本页停住时周期性提示「该去进房深挖」
 *
 * 做不到（本脚本不碰）：
 * - 无人值守自动点房、自动登录、后台 24 个房并行滚历史
 * - 当盘中买卖主信号
 *
 * 控制：
 *   window.__infoLiveMiddayWatchV1Options = { interval_ms: 90000, focus: "AB" }
 *   __infoLiveMiddayWatchStopV1()
 *   __infoLiveMiddayWatchStatusV1()
 *   __infoLiveMiddayWatchScanOnceV1()
 */
(function () {
  const WATCH_VERSION = "live_info_midday_watch_v1.1";
  // 每日盯梢范围 = A8+B14；FROZEN_OUT 不进默认 watch
  const A_ROOM_NAMES = [
    "复盘哥",
    "独家老师5号",
    "独家短线老师6号",
    "梅森",
    "顺势而为",
    "混江龙",
    "天赢居",
    "先知",
  ];
  const B_ROOM_NAMES = [
    "天机",
    "游资胖大叔",
    "潜伏王者",
    "k神",
    "周期女王",
    "格兰投研",
    "擒龙小师姐",
    "独家竞价低吸",
    "小锦鲤",
    "核心逻辑社",
    "梦幻一步",
    "新生代",
    "龙头交易猿",
    "小作文嗅嗅+机构研报",
  ];
  const FROZEN_OUT_ROOM_NAMES = [
    "机构电话会议纪要+小作文+情报",
    "机构研报资讯精选",
  ];
  const ROOM_NAME_ALIAS_MAP = {
    天机短线试更新: "天机",
    "周期女王（新一期，重新搞的）": "周期女王",
  };

  const opts = Object.assign(
    {
      interval_ms: 90000,
      focus: "AB", // "A" | "B" | "AB" | 自定义数组走 watch_names
      watch_names: null,
      beep: true,
      log_unchanged: false,
      max_alerts_keep: 80,
    },
    window.__infoLiveMiddayWatchV1Options || {}
  );

  function cleanText(text) {
    return String(text || "")
      .replace(/\u00a0/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function normalizeKnownRoomName(text) {
    const value = cleanText(text);
    if (!value) return "";
    if (ROOM_NAME_ALIAS_MAP[value]) return ROOM_NAME_ALIAS_MAP[value];
    const truncated = value.replace(/[…\.．]{1,}$/g, "").replace(/（新.*$/g, "").trim();
    if (ROOM_NAME_ALIAS_MAP[truncated]) return ROOM_NAME_ALIAS_MAP[truncated];
    if (/^周期女王/.test(value)) return "周期女王";
    if (/^天机/.test(value)) return "天机";
    return value;
  }

  function watchList() {
    if (Array.isArray(opts.watch_names) && opts.watch_names.length) {
      return opts.watch_names.map(normalizeKnownRoomName).filter(Boolean);
    }
    const f = String(opts.focus || "AB").toUpperCase();
    if (f === "A") return A_ROOM_NAMES.slice();
    if (f === "B") return B_ROOM_NAMES.slice();
    return A_ROOM_NAMES.concat(B_ROOM_NAMES);
  }

  function matchWatchName(text) {
    const value = normalizeKnownRoomName(text);
    if (!value) return "";
    const list = watchList();
    return (
      list.find((name) => value === name || value.startsWith(name) || name.startsWith(value)) ||
      ""
    );
  }

  function isVisible(el) {
    if (!(el instanceof Element)) return false;
    const style = window.getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity || "1") === 0) {
      return false;
    }
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  }

  function isLeafLike(el) {
    const text = cleanText(el.innerText || el.textContent || "");
    if (!text) return false;
    const childWithSameText = Array.from(el.children).some((child) => {
      if (!isVisible(child)) return false;
      const childText = cleanText(child.innerText || child.textContent || "");
      return childText && childText === text;
    });
    return !childWithSameText;
  }

  function hasRoomContainer(el) {
    let current = el;
    while (current && current instanceof Element) {
      if (/^room\d+$/i.test(current.id || "")) return true;
      current = current.parentElement;
    }
    return false;
  }

  function getRoomContainer(el) {
    let current = el;
    while (current && current instanceof Element) {
      if (/^room\d+$/i.test(current.id || "")) return current;
      current = current.parentElement;
    }
    return null;
  }

  function getRoomTitleCandidates() {
    const maxLeft = Math.min(window.innerWidth * 0.35, 420);
    const skipPattern =
      /历史记录|刷新|导出|下载|搜索|返回|日期|今天|昨日|更多|设置|切换|登录|退出|签到|重要提示|开通|取消/;
    return Array.from(document.querySelectorAll("body *"))
      .filter(isVisible)
      .filter(isLeafLike)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const text = cleanText(el.innerText || el.textContent || "");
        const classText = cleanText(el.className || "");
        return { el, rect, text, classText };
      })
      .filter(({ el, rect, text, classText }) => {
        return (
          hasRoomContainer(el) &&
          rect.left < maxLeft &&
          rect.width >= 80 &&
          rect.width <= 260 &&
          rect.height >= 18 &&
          rect.height <= 42 &&
          text.length >= 2 &&
          text.length <= 40 &&
          !/\b20\d{2}\/\d{2}\/\d{2}\b/.test(text) &&
          !/\b\d{2}\/\d{2}\s+\d{2}:\d{2}\b/.test(text) &&
          !/\b\d{2}:\d{2}:\d{2}\b/.test(text) &&
          !skipPattern.test(text) &&
          /text-black/.test(classText) &&
          /text-bold/.test(classText)
        );
      });
  }

  function snapshotVisiblePriorityRooms() {
    const map = {};
    for (const item of getRoomTitleCandidates()) {
      const formal = matchWatchName(item.text);
      if (!formal) continue;
      const container = getRoomContainer(item.el);
      const leafTexts = container
        ? Array.from(container.querySelectorAll("*"))
            .filter(isVisible)
            .filter(isLeafLike)
            .map((n) => cleanText(n.innerText || n.textContent || ""))
            .filter(Boolean)
        : [];
      const timeText =
        leafTexts.find((t) => /^\d{2}\/\d{2}\s+\d{2}:\d{2}$/.test(t) || /^\d{2}:\d{2}$/.test(t)) ||
        "";
      const preview =
        leafTexts
          .filter((t) => t !== item.text)
          .find(
            (t) =>
              t.length >= 2 &&
              !/^\d{2}:\d{2}/.test(t) &&
              !/^\d{2}\/\d{2}/.test(t) &&
              !/^20\d{2}/.test(t)
          ) || "";
      const fingerprint = [formal, timeText, preview.slice(0, 80)].join("||");
      // 同名只留第一条（列表里通常只一格）
      if (!map[formal]) {
        map[formal] = {
          room_anchor: formal,
          title_raw: item.text,
          latest_time_text: timeText,
          latest_preview_text: preview.slice(0, 120),
          fingerprint: fingerprint,
          is_active: /active|current|selected|focus|checked|on/i.test(item.classText),
        };
      }
    }
    return map;
  }

  function softBeep() {
    if (!opts.beep) return;
    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;
      const ctx = new Ctx();
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = "sine";
      o.frequency.value = 880;
      g.gain.value = 0.03;
      o.connect(g);
      g.connect(ctx.destination);
      o.start();
      setTimeout(() => {
        o.stop();
        ctx.close();
      }, 120);
    } catch (_e) {
      /* ignore */
    }
  }

  if (window.__infoLiveMiddayWatchTimerV1) {
    clearInterval(window.__infoLiveMiddayWatchTimerV1);
    window.__infoLiveMiddayWatchTimerV1 = null;
  }

  const state = {
    version: WATCH_VERSION,
    started_at: new Date().toISOString(),
    interval_ms: Number(opts.interval_ms) || 90000,
    focus: opts.focus,
    watch_count: watchList().length,
    scan_count: 0,
    last_scan_at: "",
    last_hits: 0,
    last_visible_priority: 0,
    previous: {},
    alerts: [],
    running: true,
  };
  window.__infoLiveMiddayWatchStateV1 = state;
  window.__infoLiveMiddayAlertsV1 = state.alerts;

  function pushAlert(entry) {
    state.alerts.unshift(entry);
    if (state.alerts.length > (opts.max_alerts_keep || 80)) {
      state.alerts.length = opts.max_alerts_keep || 80;
    }
    console.warn(
      "[midday_watch] UPDATE",
      entry.room_anchor,
      "| time:",
      entry.latest_time_text || "-",
      "| preview:",
      (entry.latest_preview_text || "").slice(0, 60)
    );
    console.warn(
      "  → 人手点进该房历史记录，粘贴 current_page 或 incremental；勿当成盘中下单信号"
    );
    softBeep();
  }

  function scanOnce(isBaseline) {
    const now = new Date().toISOString();
    const snap = snapshotVisiblePriorityRooms();
    const names = Object.keys(snap);
    state.scan_count += 1;
    state.last_scan_at = now;
    state.last_visible_priority = names.length;

    const updates = [];
    if (!isBaseline) {
      for (const name of names) {
        const cur = snap[name];
        const prev = state.previous[name];
        if (!prev) {
          updates.push(Object.assign({ reason: "newly_visible" }, cur));
        } else if (prev.fingerprint !== cur.fingerprint) {
          updates.push(
            Object.assign(
              { reason: "preview_or_time_changed", prev_preview: prev.latest_preview_text },
              cur
            )
          );
        }
      }
    }

    for (const u of updates) {
      pushAlert(
        Object.assign(
          {
            ts: now,
            action_hint:
              '__infoLiveApplyCurrentPageForRoom("' +
              u.room_anchor +
              '") 后粘贴 current_page；或 __infoLiveApplyIncrementalForRoom("' +
              u.room_anchor +
              '") 后粘贴 incremental',
          },
          u
        )
      );
    }
    state.last_hits = updates.length;
    state.previous = snap;

    if (isBaseline) {
      console.log(
        WATCH_VERSION,
        "baseline ok. visible A/B on screen:",
        names.length,
        "/",
        state.watch_count,
        names.slice(0, 12).join(" | ") + (names.length > 12 ? " ..." : "")
      );
      console.log(
        "说明：左侧列表未滚出的房间本次看不到；可手动滚一下列表扩大可见区。"
      );
    } else if (opts.log_unchanged || updates.length) {
      console.log(
        "[midday_watch] scan#" + state.scan_count,
        "visible=",
        names.length,
        "updates=",
        updates.length
      );
    }
    return { snap, updates };
  }

  window.__infoLiveMiddayWatchStopV1 = function () {
    if (window.__infoLiveMiddayWatchTimerV1) {
      clearInterval(window.__infoLiveMiddayWatchTimerV1);
      window.__infoLiveMiddayWatchTimerV1 = null;
    }
    state.running = false;
    console.log(WATCH_VERSION, "stopped");
    return state;
  };

  window.__infoLiveMiddayWatchStatusV1 = function () {
    console.log(state);
    return state;
  };

  window.__infoLiveMiddayWatchScanOnceV1 = function () {
    return scanOnce(false);
  };

  // 启动
  scanOnce(true);
  window.__infoLiveMiddayWatchTimerV1 = setInterval(function () {
    try {
      scanOnce(false);
    } catch (err) {
      console.error("[midday_watch] scan error", err);
    }
  }, state.interval_ms);

  console.log(
    WATCH_VERSION,
    "running every",
    state.interval_ms,
    "ms | focus=",
    opts.focus,
    "| stop: __infoLiveMiddayWatchStopV1()"
  );
  return state;
})();
