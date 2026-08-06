(function () {
  const EXPORT_VERSION = "live_info_current_page_export_v1.5";
  const ROOM_SPEAKER_ALIAS_MAP = {
    "至尊宝": "孙悟空金牌",
    "陈子瞻": "龙头交易猿",
  };
  // Canonical room names for first-batch pinned / template rooms.
  // Expand later when 置顶名单正式冻结.
  const ROOM_NAME_ALIAS_MAP = {
    "天机短线试更新": "天机",
    "周期女王（新一期，重新搞的）": "周期女王",
  };
  const PRIORITY_ROOM_NAMES = [
    "格兰投研",
    "周期女王",
    "天机",
    "天机短线试更新",
    "龙头交易猿",
    "孙悟空金牌",
  ];
  // Short names that often win sidebar/hashtag contests due to bot mixed tags.
  const DRIFT_ANCHOR_NAMES = new Set(["k神", "先知", "浮光", "知行合一"]);
  const runtimePageOptions = window.__infoLiveCurrentPageExportV1Options || {};

  function cleanText(text) {
    return String(text || "")
      .replace(/\u00a0/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function normalizeDateText(text) {
    const raw = cleanText(text);
    const match = raw.match(/(\d{4})[\/-](\d{1,2})[\/-](\d{1,2})/);
    if (!match) return raw;
    return `${match[1]}/${String(match[2]).padStart(2, "0")}/${String(match[3]).padStart(2, "0")}`;
  }

  function intersectsRect(a, b) {
    return !(
      a.right <= b.left ||
      a.left >= b.right ||
      a.bottom <= b.top ||
      a.top >= b.bottom
    );
  }

  function getClipAncestors(el) {
    const ancestors = [];
    let current = el.parentElement;
    while (current && current instanceof Element && current !== document.body) {
      const style = window.getComputedStyle(current);
      const overflowText = `${style.overflow} ${style.overflowY} ${style.overflowX}`;
      if (/(auto|scroll|hidden|overlay)/i.test(overflowText)) ancestors.push(current);
      current = current.parentElement;
    }
    return ancestors;
  }

  function isVisible(el) {
    if (!(el instanceof Element)) return false;
    const style = window.getComputedStyle(el);
    if (
      style.display === "none" ||
      style.visibility === "hidden" ||
      Number(style.opacity || "1") === 0
    ) {
      return false;
    }
    const rect = el.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return false;
    const viewportRect = {
      left: 0,
      top: 0,
      right: window.innerWidth,
      bottom: window.innerHeight,
    };
    if (!intersectsRect(rect, viewportRect)) return false;
    for (const ancestor of getClipAncestors(el)) {
      if (!intersectsRect(rect, ancestor.getBoundingClientRect())) return false;
    }
    return true;
  }

  function getText(el) {
    return cleanText(el && (el.innerText || el.textContent || ""));
  }

  function parseDateTime(text) {
    const match = cleanText(text).match(
      /(20\d{2}[\/-]\d{1,2}[\/-]\d{1,2})\s+(\d{2}:\d{2}(?::\d{2})?)/
    );
    if (!match) return null;
    return {
      display_date: normalizeDateText(match[1]),
      display_time: match[2],
    };
  }

  function parseTimeToken(text) {
    const m = cleanText(text).match(/\b(\d{2}:\d{2}(?::\d{2})?)\b/);
    return m ? m[1] : "";
  }

  function isWeakRoomAnchor(text) {
    const value = cleanText(text);
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
      /^MX技术小筑$/i.test(value)
    );
  }

  function isUiNoiseText(text, roomAnchor) {
    const value = cleanText(text);
    if (!value) return true;
    if (roomAnchor && value === roomAnchor) return true;
    if (/^讲师$/.test(value) || /^老师$/.test(value)) return true;
    // Pure datetime leaf is chrome, not body.
    if (
      parseDateTime(value) &&
      /^(?:讲师\s+|老师\s+)?20\d{2}[\/-]\d{1,2}[\/-]\d{1,2}\s+\d{2}:\d{2}(?::\d{2})?$/.test(value)
    ) {
      return true;
    }
    if (/^\d{2}:\d{2}(?::\d{2})?$/.test(value)) return true;
    // Only treat SHORT chrome labels as UI noise.
    // Do NOT reuse isWeakRoomAnchor here: length>30 / "！" would kill real message bodies.
    if (value.length > 40) return false;
    return /^(历史记录|倒序观看历史记录|正序观看历史记录|倒序观看|正序观看|直播间列表|搜索直播间名称|搜索直播间消息|搜索|选择日期|时间|刷新|导出|下载|返回|公告|今天|昨日)$/.test(
      value
    ) || /历史记录|直播间列表|搜索直播间名称|搜索直播间消息|选择日期|倒序观看|正序观看/.test(value);
  }

  function normalizeKnownRoomName(text) {
    const value = cleanText(text);
    if (!value) return "";
    if (ROOM_NAME_ALIAS_MAP[value]) return ROOM_NAME_ALIAS_MAP[value];
    // Sidebar titles may truncate with ellipsis / fullwidth dots.
    const truncated = value.replace(/[…\.．]{1,}$/g, "").replace(/（新.*$/g, "").trim();
    if (ROOM_NAME_ALIAS_MAP[truncated]) return ROOM_NAME_ALIAS_MAP[truncated];
    if (/^周期女王/.test(value)) return "周期女王";
    if (/^天机/.test(value)) return "天机";
    return value;
  }

  function isPriorityRoomName(text) {
    const value = normalizeKnownRoomName(text);
    if (!value) return false;
    return PRIORITY_ROOM_NAMES.some((name) => value === name || value.startsWith(name) || name.startsWith(value));
  }

  function isDriftAnchorName(text) {
    return DRIFT_ANCHOR_NAMES.has(cleanText(text));
  }

  function isPromoNoiseText(text) {
    const value = cleanText(text);
    if (!value) return true;
    if (/^更多资讯加微信好友/i.test(value)) return true;
    if (/加微信好友aa\d+/i.test(value) && value.length <= 40) return true;
    if (/^防止失联QQ群\d+$/i.test(value)) return true;
    if (/^QQ群\d+$/i.test(value)) return true;
    // Pure emoji / sticker hashtags that bots inject into tag streams.
    if (/^#(捂脸|破涕为笑|流泪|笑哭|微笑)#$/.test(value)) return true;
    if (/^(捂脸|破涕为笑|流泪)$/.test(value)) return true;
    return false;
  }

  function stripPromoFragments(text) {
    return cleanText(text)
      .replace(/更多资讯加微信好友aa\d+/gi, " ")
      .replace(/防止失联QQ群\d+/gi, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function composeCoreBodyText(bodyTexts, cardRoot) {
    const filtered = (bodyTexts || [])
      .map((t) => cleanText(t))
      .filter(Boolean)
      .filter((t) => !isPromoNoiseText(t));

    let core = "";
    if (filtered.length) {
      // Prefer the longest substantive leaf; join others only if they add meaningful length.
      const ranked = filtered.slice().sort((a, b) => b.length - a.length);
      const longest = ranked[0];
      if (longest.length >= 40) {
        const extras = ranked
          .slice(1)
          .filter((t) => t.length >= 24 && !longest.includes(t))
          .slice(0, 3);
        core = [longest].concat(extras).join(" ");
      } else {
        core = filtered.join(" ");
      }
    }

    if (!core || core.length < 8) {
      const raw = stripPromoFragments(getText(cardRoot));
      // Drop leading chrome datetime / speaker chrome if present as only short residue.
      core = stripPromoFragments(raw);
    } else {
      core = stripPromoFragments(core);
    }

    return stripSpeakerLabel(core);
  }

  function stripSpeakerLabel(text) {
    return cleanText(text)
      .replace(/^讲师\s*/g, "")
      .replace(/^老师\s*/g, "")
      .replace(/^讲师[:：]\s*/g, "")
      .replace(/^老师[:：]\s*/g, "");
  }

  function simplifyRoomAnchor(text) {
    const value = stripSpeakerLabel(text);
    if (!value) return "";
    if (/^20\d{2}[\/-]\d{1,2}[\/-]\d{1,2}(?:\s+\d{2}:\d{2}(?::\d{2})?)?$/.test(value)) return "";
    if (/^\d{2}:\d{2}(?::\d{2})?$/.test(value)) return "";
    if (value.length > 30) return "";

    const exactName = value.match(/^([\u4e00-\u9fa5A-Za-z0-9（）()·\-_]{2,20})\s+\d{2}:\d{2}(?::\d{2})?\b/);
    if (exactName) return cleanText(exactName[1]);

    const shortName = value.match(/^([\u4e00-\u9fa5A-Za-z0-9（）()·\-_]{2,20})/);
    if (shortName) return cleanText(shortName[1]);

    return value;
  }

  function extractLeadingName(text) {
    const value = stripSpeakerLabel(text);
    if (!value) return "";
    // Prefer known speaker aliases first (avoid "至尊宝龟兔这个模式..." greedily matching 20 chars).
    for (const alias of Object.keys(ROOM_SPEAKER_ALIAS_MAP)) {
      if (value === alias || value.startsWith(alias)) return alias;
    }
    // Short speaker/room prefix only: stop before punctuation or long prose.
    const m = value.match(/^([\u4e00-\u9fa5A-Za-z0-9（）()·\-_]{2,8})(?=$|[：:\s，,。！!？?])/);
    return m ? cleanText(m[1]) : "";
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

  function isScrollableContainer(el) {
    if (!(el instanceof HTMLElement)) return false;
    if (/uni-scroll-view/i.test(el.tagName) || /uni-scroll-view/i.test(el.className || "")) return true;
    const style = window.getComputedStyle(el);
    const overflowY = style.overflowY || style.overflow || "";
    if (/(auto|scroll|overlay)/i.test(overflowY)) return true;
    const overflow = (el.scrollHeight || 0) - (el.clientHeight || 0);
    return overflow > 80;
  }

  function isLikelyCardOnly(el, rect, textLen) {
    const className = cleanText((el && el.className) || "");
    if (/cu-card/i.test(className)) return true;
    if (rect.height < 260 && textLen < 260) return true;
    return false;
  }

  function upgradeToContainerAncestor(el) {
    let current = el;
    let best = el;
    let bestScore = -Infinity;
    let depth = 0;
    while (current && current instanceof Element && current !== document.body && depth < 14) {
      const rect = current.getBoundingClientRect();
      const textLen = getText(current).length;
      const className = cleanText(current.className || "");
      let score = 0;
      if (rect.left > 350 && rect.width > 320 && rect.height > 140) {
        score += Math.min(textLen, 1600);
        if (isScrollableContainer(current)) score += 260;
        if (/uni-scroll-view/i.test(current.tagName) || /uni-scroll-view/i.test(className)) score += 160;
        if (rect.height > 500) score += 80;
        if (rect.width > 700) score += 40;
        if (/cu-card/i.test(className)) score -= 300;
        if (score > bestScore) {
          bestScore = score;
          best = current;
        }
      }
      current = current.parentElement;
      depth += 1;
    }
    return best;
  }

  function chooseContentRoot() {
    const candidates = Array.from(document.querySelectorAll("body *"))
      .filter(isVisible)
      .map((el) => ({
        el,
        rect: el.getBoundingClientRect(),
        text: getText(el),
      }))
      .filter((item) => item.rect.left > 350 && item.rect.width > 320 && item.rect.height > 140 && item.text.length > 50);

    const scored = candidates.map((item) => {
      const className = cleanText(item.el.className || "");
      let score = Math.min(item.text.length, 1600);
      if (isScrollableContainer(item.el)) score += 260;
      if (/uni-scroll-view/i.test(item.el.tagName) || /uni-scroll-view/i.test(className)) score += 160;
      if (item.rect.height > 500) score += 80;
      if (item.rect.width > 700) score += 40;
      if (/cu-card/i.test(className)) score -= 300;
      if (isLikelyCardOnly(item.el, item.rect, item.text.length)) score -= 180;
      return { ...item, className, score };
    }).sort((a, b) => b.score - a.score);

    const picked = scored[0];
    if (!picked) return document.body;
    if (/cu-card/i.test(picked.className) || isLikelyCardOnly(picked.el, picked.rect, picked.text.length)) {
      return upgradeToContainerAncestor(picked.el);
    }
    return picked.el;
  }

  function chooseTopCenterTitle() {
    const center = window.innerWidth / 2;
    const candidates = Array.from(document.querySelectorAll("body *"))
      .filter((el) => el instanceof HTMLElement)
      .filter(isVisible)
      .map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          el,
          rect,
          text: getText(el),
        };
      })
      .filter((item) => item.text && item.rect.top >= 0 && item.rect.top < 120 && item.rect.width > 60)
      .filter((item) => Math.abs((item.rect.left + item.rect.right) / 2 - center) < 220)
      .filter((item) => !isWeakRoomAnchor(item.text));

    candidates.sort((a, b) => {
      const distA = Math.abs((a.rect.left + a.rect.right) / 2 - center);
      const distB = Math.abs((b.rect.left + b.rect.right) / 2 - center);
      if (distA !== distB) return distA - distB;
      return a.rect.top - b.rect.top;
    });

    return candidates[0]?.text || "";
  }

  function chooseActiveLeftRoom() {
    const leftCandidates = Array.from(document.querySelectorAll("body *"))
      .filter((el) => el instanceof HTMLElement)
      .filter(isVisible)
      .map((el) => ({
        el,
        rect: el.getBoundingClientRect(),
        text: cleanText(getText(el)),
      }))
      .filter((item) => item.rect.left >= 0 && item.rect.left < 330 && item.rect.width > 60 && item.rect.height > 20)
      .filter((item) => {
        const text = item.text;
        if (isWeakRoomAnchor(text)) return false;
        // Sidebar preview snippets often look like: "先知 2027/01/19 [图片] 08/05 23:13"
        if (/20\d{2}[\/-]\d{1,2}[\/-]\d{1,2}/.test(text)) return false;
        if (/\[图片\]/.test(text)) return false;
        if (/\d{2}:\d{2}/.test(text) && text.length > 12) return false;
        return text.length >= 2 && text.length <= 28;
      })
      .map((item) => {
        const className = (item.el.className || "").toString();
        const active = /active|current|selected|focus|on|checked/i.test(className) ? 1 : 0;
        const priority = isPriorityRoomName(item.text) ? 1 : 0;
        const drift = isDriftAnchorName(item.text) ? 1 : 0;
        // Prefer pure room titles (not long previews). Soft length preference, not hard shortest-wins.
        const lengthScore = item.text.length <= 16 ? 8 : Math.max(0, 20 - item.text.length);
        const score = active * 100 + priority * 60 - drift * 40 + lengthScore + Math.min(item.rect.width, 240) / 20;
        return { ...item, active, priority, drift, score };
      });

    leftCandidates.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return a.rect.top - b.rect.top;
    });

    const picked = leftCandidates[0];
    return picked ? normalizeKnownRoomName(picked.text) : "";
  }

  function isLeafLike(el) {
    const text = getText(el);
    if (!text) return false;
    return !Array.from(el.children).some((child) => isVisible(child) && getText(child) === text);
  }

  function getLeafEntries(root) {
    return Array.from(root.querySelectorAll("*"))
      .filter(isVisible)
      .filter(isLeafLike)
      .map((el) => ({
        el,
        text: getText(el),
        rect: el.getBoundingClientRect(),
      }))
      .filter((entry) => entry.text);
  }

  function findMessageCardRoot(anchorEl, contentRoot, roomAnchor) {
    const candidates = [];
    let current = anchorEl;
    while (current && current instanceof Element && current !== contentRoot) {
      const rect = current.getBoundingClientRect();
      if (rect.width > 320 && rect.height > 40 && rect.left > 20) {
        const leafEntries = getLeafEntries(current);
        const texts = leafEntries.map((entry) => entry.text);
        const timeCount = texts.filter((text) => parseDateTime(text)).length;
        const bodyCount = texts.filter((text) => !parseDateTime(text) && !isUiNoiseText(text, roomAnchor)).length;
        const className = cleanText(current.className || "");
        let score = 0;
        score += Math.min(timeCount, 3) * 20;
        score += Math.min(bodyCount, 6) * 12;
        if (/cu-card/i.test(className)) score += 80;
        if (rect.height >= 80) score += 20;
        if (rect.height >= 110) score += 10;
        if (current === contentRoot) score -= 120;
        candidates.push({ el: current, score });
      }
      current = current.parentElement;
    }
    candidates.sort((a, b) => b.score - a.score);
    return candidates[0]?.el || anchorEl.parentElement || anchorEl;
  }

  function extractCardMessage(cardRoot, roomAnchor, fallbackDt) {
    if (!(cardRoot instanceof Element)) return null;
    const leafEntries = getLeafEntries(cardRoot);
    const timeOnlyPattern = /^\d{2}:\d{2}(?::\d{2})?$/;
    const timeTokenPattern = /\b\d{2}:\d{2}(?::\d{2})?\b/;
    const timeEntry = leafEntries.find(
      (entry) => parseDateTime(entry.text) || timeOnlyPattern.test(entry.text) || timeTokenPattern.test(entry.text)
    );
    const dtFromEntry = timeEntry ? parseDateTime(timeEntry.text) : null;
    const timeToken = timeEntry ? parseTimeToken(timeEntry.text) : "";
    const dt = dtFromEntry || (fallbackDt || null) || (timeToken ? { display_date: "", display_time: timeToken } : null);
    if (!dt || (!dt.display_time && !dt.display_date)) return null;

    const bodyTexts = leafEntries
      .map((entry) => entry.text)
      .filter((text) => !parseDateTime(text))
      .filter((text) => !timeOnlyPattern.test(text))
      .filter((text) => !isUiNoiseText(text, roomAnchor));

    const text = composeCoreBodyText(bodyTexts, cardRoot);
    if (!text || text.length < 4) return null;
    // If only promo survived stripping, drop the card (avoid 天机-style false bodies).
    if (isPromoNoiseText(text) && text.length <= 40) return null;

    const rect = cardRoot.getBoundingClientRect();
    return {
      display_date: dt.display_date || "",
      display_time: dt.display_time || "",
      text,
      card_rect: {
        top: Math.round(rect.top),
        left: Math.round(rect.left),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      },
    };
  }

  function expandMergedCardMessages(message) {
    if (!message || !message.text) return [];
    const text = cleanText(message.text);
    // 格兰等房偶发一张卡粘连多条；按日期时间边界拆成多条核心记录。
    if (text.length < 600) return [message];
    const dtRe = /(20\d{2}[\/-]\d{1,2}[\/-]\d{1,2})\s+(\d{2}:\d{2}(?::\d{2})?)/g;
    const hits = Array.from(text.matchAll(dtRe));
    if (hits.length < 2) return [message];

    const parts = [];
    for (let i = 0; i < hits.length; i += 1) {
      const start = hits[i].index || 0;
      const end = i + 1 < hits.length ? hits[i + 1].index : text.length;
      const chunk = cleanText(text.slice(start, end));
      if (!chunk || chunk.length < 8) continue;
      const body = stripSpeakerLabel(
        stripPromoFragments(chunk.replace(hits[i][0], " ").replace(/^老师\s*/g, " "))
      );
      if (!body || body.length < 4 || isPromoNoiseText(body)) continue;
      parts.push({
        display_date: normalizeDateText(hits[i][1]),
        display_time: hits[i][2],
        text: body,
        card_rect: message.card_rect,
      });
    }
    return parts.length >= 2 ? parts : [message];
  }

  function sortMessagesByViewport(messages) {
    return (messages || []).slice().sort((a, b) => {
      const topA = a && a.card_rect ? Number(a.card_rect.top) : 0;
      const topB = b && b.card_rect ? Number(b.card_rect.top) : 0;
      if (topA !== topB) return topA - topB;
      const left = `${a.display_date || ""} ${a.display_time || ""}`;
      const right = `${b.display_date || ""} ${b.display_time || ""}`;
      if (left < right) return -1;
      if (left > right) return 1;
      return 0;
    });
  }

  function extractVisibleMessagesFromCuCards(contentRoot, roomAnchor) {
    // Prefer cards under contentRoot; if scroll-view root contains no cards,
    // fall back to right-pane cards on the page (same as probe's wider root).
    const scopes = [contentRoot, document.body];
    let cards = [];
    for (const scope of scopes) {
      if (!(scope instanceof Element)) continue;
      cards = Array.from(scope.querySelectorAll("*"))
        .filter((el) => el instanceof HTMLElement && isVisible(el))
        .filter((el) => /(?:^|\s)cu-card(?:\s|$)/i.test(cleanText(el.className || "")))
        .filter((el) => {
          const rect = el.getBoundingClientRect();
          return rect.width > 320 && rect.height > 60 && rect.left > 350;
        });
      if (cards.length) break;
    }

    const map = new Map();
    for (const cardRoot of cards) {
      const message = extractCardMessage(cardRoot, roomAnchor, null);
      if (!message || !message.text || message.text.length < 4) continue;
      for (const part of expandMergedCardMessages(message)) {
        const key = `${part.display_date} ${part.display_time} ${part.text.slice(0, 80)}`;
        if (!map.has(key)) map.set(key, part);
      }
    }
    return sortMessagesByViewport(Array.from(map.values()));
  }

  function extractVisibleMessages(contentRoot, roomAnchor) {
    const fromCards = extractVisibleMessagesFromCuCards(contentRoot, roomAnchor);
    if (fromCards.length >= 1) return fromCards;

    const leafEntries = getLeafEntries(contentRoot);
    const dtPattern = /20\d{2}[\/-]\d{1,2}[\/-]\d{1,2}\s+\d{2}:\d{2}(?::\d{2})?/;
    const dateOnlyPattern = /^20\d{2}[\/-]\d{1,2}[\/-]\d{1,2}$/;
    const timeOnlyPattern = /^\d{2}:\d{2}(?::\d{2})?$/;
    const timeTokenPattern = /\b\d{2}:\d{2}(?::\d{2})?\b/;
    const dateTokenPattern = /20\d{2}[\/-]\d{1,2}[\/-]\d{1,2}/;

    const rootDateHintEntry = leafEntries.find((entry) => dateTokenPattern.test(entry.text));
    const rootDateHint = rootDateHintEntry
      ? normalizeDateText(cleanText(rootDateHintEntry.text).match(dateTokenPattern)?.[0] || "")
      : "";

    const dateOnlyAnchors = leafEntries
      .filter((entry) => dateOnlyPattern.test(entry.text))
      .sort((a, b) => a.rect.top - b.rect.top);

    function nearestDateForTop(top) {
      let best = "";
      for (const d of dateOnlyAnchors) {
        if (d.rect.top <= top) best = normalizeDateText(d.text);
        else break;
      }
      return best || rootDateHint;
    }

    let timeAnchors = leafEntries
      .filter((entry) => dtPattern.test(entry.text))
      .sort((a, b) => a.rect.top - b.rect.top);

    let useTimeOnlyAnchors = false;
    if (!timeAnchors.length) {
      timeAnchors = leafEntries
        .filter((entry) => timeOnlyPattern.test(entry.text))
        .sort((a, b) => a.rect.top - b.rect.top);
      useTimeOnlyAnchors = true;
    }

    if (!timeAnchors.length) {
      timeAnchors = leafEntries
        .filter((entry) => timeTokenPattern.test(entry.text))
        .sort((a, b) => a.rect.top - b.rect.top);
      useTimeOnlyAnchors = true;
    }

    if (!timeAnchors.length) {
      const fallback = Array.from(contentRoot.querySelectorAll("*"))
        .filter((el) => el instanceof HTMLElement)
        .filter(isVisible)
        .slice(0, 4000)
        .map((el) => ({
          el,
          text: getText(el),
          rect: el.getBoundingClientRect(),
        }))
        .filter((entry) => entry.rect.left > 350 && entry.rect.width > 80 && entry.rect.height > 16)
        .filter((entry) => dtPattern.test(entry.text) || timeOnlyPattern.test(entry.text) || timeTokenPattern.test(entry.text))
        .sort((a, b) => a.rect.top - b.rect.top);
      timeAnchors = fallback;
      useTimeOnlyAnchors = timeAnchors.every((entry) => !dtPattern.test(entry.text));
    }

    if (!timeAnchors.length) {
      const cardCandidates = Array.from(contentRoot.querySelectorAll("*"))
        .filter((el) => el instanceof HTMLElement && isVisible(el))
        .filter((el) => {
          const className = cleanText(el.className || "");
          const rect = el.getBoundingClientRect();
          if (/cu-card/i.test(className) && rect.width > 320 && rect.height > 60) return true;
          if (
            rect.width > 320 &&
            rect.height > 80 &&
            rect.left > 20 &&
            !isScrollableContainer(el) &&
            getLeafEntries(el).length >= 2
          ) {
            const texts = getLeafEntries(el).map((e) => e.text);
            const hasAnyTime = texts.some((t) => timeTokenPattern.test(t) || dtPattern.test(t));
            if (hasAnyTime) return true;
          }
          return false;
        })
        .slice(0, 120)
        .map((el) => {
          const cardRoot = el;
          let fallbackDt = null;
          const leaves = getLeafEntries(cardRoot);
          const dtHit = leaves.find((e) => dtPattern.test(e.text));
          if (dtHit) fallbackDt = parseDateTime(dtHit.text);
          if (!fallbackDt) {
            const timeOnlyHit = leaves.find((e) => timeOnlyPattern.test(e.text) || timeTokenPattern.test(e.text));
            if (timeOnlyHit) {
              fallbackDt = {
                display_date: nearestDateForTop(timeOnlyHit.rect.top),
                display_time: timeOnlyPattern.test(timeOnlyHit.text) ? timeOnlyHit.text : parseTimeToken(timeOnlyHit.text),
              };
            }
          }
          const message = extractCardMessage(cardRoot, roomAnchor, fallbackDt);
          return { el, message };
        })
        .filter((item) => item.message);
      const unique = new Map();
      for (const item of cardCandidates) {
        const m = item.message;
        const key = `${m.display_date} ${m.display_time} ${m.text.slice(0, 80)}`;
        if (!unique.has(key)) unique.set(key, m);
      }
      return sortMessagesByViewport(Array.from(unique.values()));
    }

    const map = new Map();
    for (const anchor of timeAnchors) {
      const cardRoot = findMessageCardRoot(anchor.el, contentRoot, roomAnchor);
      let fallbackDt = null;
      if (useTimeOnlyAnchors && !dtPattern.test(anchor.text)) {
        fallbackDt = {
          display_date: nearestDateForTop(anchor.rect.top),
          display_time: timeOnlyPattern.test(anchor.text) ? anchor.text : parseTimeToken(anchor.text),
        };
      } else if (dtPattern.test(anchor.text)) {
        fallbackDt = parseDateTime(anchor.text);
      }
      const message = extractCardMessage(cardRoot, roomAnchor, fallbackDt);
      if (!message) continue;
      const key = `${message.display_date} ${message.display_time} ${message.text.slice(0, 80)}`;
      if (!map.has(key)) map.set(key, message);
    }

    if (map.size < 2) {
      const allVisibleNodes = Array.from(contentRoot.querySelectorAll("*"))
        .filter((el) => el instanceof HTMLElement && isVisible(el))
        .slice(0, 5000)
        .map((el) => ({
          el,
          text: getText(el),
          rect: el.getBoundingClientRect(),
        }))
        .filter((item) => item.rect.left > 350 && item.rect.width > 200 && item.rect.height > 24);

      const timeAnchorRows = allVisibleNodes
        .filter((item) => item.text && item.text.length < 80)
        .map((item) => {
          const text = item.text;
          const dtFull = parseDateTime(text);
          if (dtFull) return { ...item, dt: dtFull, kind: "full" };
          const tToken = parseTimeToken(text);
          if (tToken) {
            const dateHint = nearestDateForTop(item.rect.top);
            return {
              ...item,
              dt: { display_date: dateHint, display_time: tToken },
              kind: "timeonly",
            };
          }
          if (dateTokenPattern.test(text)) {
            const d = cleanText(text).match(dateTokenPattern)?.[0] || "";
            return {
              ...item,
              dt: { display_date: normalizeDateText(d), display_time: "" },
              kind: "dateonly",
            };
          }
          return null;
        })
        .filter(Boolean)
        .sort((a, b) => a.rect.top - b.rect.top);

      const bodyCandidates = allVisibleNodes
        .filter((item) => {
          const t = item.text;
          if (!t || t.length < 18) return false;
          if (isUiNoiseText(t, roomAnchor)) return false;
          if (dtPattern.test(t) && t.length < 40) return false;
          if (timeOnlyPattern.test(t)) return false;
          if (/^讲师\s*[:：]?\s*$/.test(t)) return false;
          if (/^讲师\s+20\d{2}[\/-]\d{1,2}/.test(t) && t.length < 50) return false;
          const className = cleanText(item.el.className || "");
          if (/cu-card/i.test(className) && item.rect.height < 70) return false;
          return true;
        })
        .sort((a, b) => a.rect.top - b.rect.top);

      function nearestTimeAnchorForBody(bodyItem) {
        const bodyTop = bodyItem.rect.top;
        let best = null;
        let bestDist = Infinity;
        for (const t of timeAnchorRows) {
          if (!t.dt || (!t.dt.display_time && !t.dt.display_date)) continue;
          const tTop = t.rect.top;
          const d = Math.abs(tTop - bodyTop);
          if (d < bestDist && d < 360) {
            bestDist = d;
            best = t;
          }
        }
        return best;
      }

      for (const body of bodyCandidates) {
        const matched = nearestTimeAnchorForBody(body);
        if (!matched || !matched.dt) continue;
        const dt = matched.dt;
        const bodyText = stripSpeakerLabel(body.text);
        if (!bodyText || bodyText.length < 14) continue;
        const display_date = dt.display_date || nearestDateForTop(body.rect.top);
        const display_time = dt.display_time || "";
        const rect = body.rect;
        const msg = {
          display_date,
          display_time,
          text: bodyText,
          card_rect: {
            top: Math.round(rect.top),
            left: Math.round(rect.left),
            width: Math.round(rect.width),
            height: Math.round(rect.height),
          },
        };
        const key = `${msg.display_date} ${msg.display_time} ${msg.text.slice(0, 80)}`;
        if (!map.has(key)) map.set(key, msg);
      }
    }

    return sortMessagesByViewport(Array.from(map.values()));
  }

  function inferRoomAnchorByHashTag(visibleMessages) {
    const freq = {};
    for (const item of visibleMessages || []) {
      const text = cleanText((item && item.text) || "");
      const matches = text.matchAll(/#([^#\n]{2,30})#/g);
      for (const m of matches) {
        const raw = cleanText(m[1] || "");
        const name = normalizeKnownRoomName(raw);
        if (!name || isWeakRoomAnchor(name)) continue;
        // Ignore generic / strategy / promo tags that are not room names.
        if (/^(嗅嗅信息|重要提示|素材来自朋友贡献|我承认我不行)$/.test(name)) continue;
        if (isDriftAnchorName(name) && !isPriorityRoomName(name)) continue;
        if (name.length > 16 && !isPriorityRoomName(name)) continue;
        freq[name] = (freq[name] || 0) + 1;
      }
    }
    const ranked = Object.entries(freq).sort((a, b) => {
      const pa = isPriorityRoomName(a[0]) ? 1 : 0;
      const pb = isPriorityRoomName(b[0]) ? 1 : 0;
      if (pb !== pa) return pb - pa;
      return b[1] - a[1];
    });
    const top = ranked[0];
    if (!top) return "";
    const [name, count] = top;
    return count >= 1 ? name : "";
  }

  function inferRoomAnchorFromMessages(initialRoomAnchor, visibleMessages, topicAnchor) {
    const forced = normalizeKnownRoomName(runtimePageOptions.forced_room_anchor || runtimePageOptions.forcedRoomAnchor || "");
    if (forced && !isWeakRoomAnchor(forced)) return forced;

    // 1) Known speaker alias (至尊宝 -> 孙悟空金牌 / 陈子瞻 -> 龙头交易猿)
    const aliasRoom = inferRoomAnchorBySpeakerAlias("", visibleMessages);
    if (aliasRoom) return aliasRoom;

    const initialNorm = normalizeKnownRoomName(initialRoomAnchor);
    // 2) If sidebar/title already resolves to a priority template room, keep it.
    //    Do not let bot-injected mixed tags override (周期女王/天机 现场教训).
    if (initialNorm && isPriorityRoomName(initialNorm) && !isDriftAnchorName(initialNorm)) {
      return normalizeKnownRoomName(initialNorm);
    }

    // 3) Majority / priority #房间名# in bodies (still demote drift names)
    const hashRoom = inferRoomAnchorByHashTag(visibleMessages);
    if (hashRoom) return hashRoom;

    if (topicAnchor) {
      const topicHash = cleanText(topicAnchor).match(/#([^#\n]{2,30})#/);
      if (topicHash) {
        const topicName = normalizeKnownRoomName(topicHash[1]);
        if (topicName && !isWeakRoomAnchor(topicName) && !isDriftAnchorName(topicName)) return topicName;
      }
    }

    if (initialNorm && !isWeakRoomAnchor(initialNorm)) {
      const simplified = simplifyRoomAnchor(initialNorm);
      return normalizeKnownRoomName(simplified || initialNorm);
    }

    const sources = [];
    if (topicAnchor) sources.push(topicAnchor);
    for (const item of visibleMessages || []) {
      if (item && item.text) sources.push(item.text);
    }

    const normalizedSources = sources
      .map((text) => stripSpeakerLabel(text))
      .filter(Boolean);

    const prefixMatch = normalizedSources
      .map((text) => text.match(/^([\u4e00-\u9fa5A-Za-z0-9（）()·\-_]{2,20})\s+\d{2}:\d{2}(?::\d{2})?\b/))
      .find(Boolean);
    if (prefixMatch && !isWeakRoomAnchor(prefixMatch[1]) && !isDriftAnchorName(prefixMatch[1])) {
      return normalizeKnownRoomName(prefixMatch[1]);
    }

    return initialNorm || "";
  }

  function detectHistoryViewOrder(contentRoot) {
    const scopeText = getText(contentRoot || document.body).slice(0, 2500);
    const bodyText = getText(document.body).slice(0, 4000);
    const text = `${scopeText} ${bodyText}`;
    // UI often shows the active mode label like "倒序观看历史记录".
    if (/倒序观看/.test(text) && !/正序观看历史记录/.test(text)) return "reverse";
    if (/正序观看/.test(text) && !/倒序观看历史记录/.test(text)) return "forward";
    if (/倒序观看/.test(text)) return "reverse";
    if (/正序观看/.test(text)) return "forward";
    // Default for this site's history pages: chat-like newest toward bottom / reverse reading.
    return "reverse";
  }

  function messageTimeKey(item) {
    const date = cleanText((item && item.display_date) || "");
    const time = cleanText((item && item.display_time) || "");
    const normalizedDate = normalizeDateText(date).replace(/\//g, "-");
    const normalizedTime = time.length === 5 ? `${time}:00` : time;
    return `${normalizedDate} ${normalizedTime}`;
  }

  function choosePrimaryMessage(visibleMessages, viewOrder) {
    const list = (visibleMessages || []).filter((item) => item && item.text);
    if (!list.length) return null;
    const order = viewOrder || "reverse";
    const ranked = list.slice().sort((a, b) => {
      const keyA = messageTimeKey(a);
      const keyB = messageTimeKey(b);
      if (keyA !== keyB) return keyA < keyB ? -1 : 1;
      const topA = a.card_rect ? Number(a.card_rect.top) : 0;
      const topB = b.card_rect ? Number(b.card_rect.top) : 0;
      return topA - topB;
    });
    // 倒序：顶层摘要取“当前可见里时间最新”的一条（你肉眼说的第一条/最新）。
    // 正序：取时间最早 / 视口偏上的一条。
    if (order === "forward") return ranked[0];
    return ranked[ranked.length - 1];
  }

  function chooseTopicAnchor(primaryMessage, roomAnchor) {
    if (roomAnchor && !isWeakRoomAnchor(roomAnchor)) return `#${roomAnchor}#`;
    if (!primaryMessage || !primaryMessage.text) return "";
    return cleanText(primaryMessage.text).slice(0, 80);
  }

  function chooseImageEvidence(contentRoot) {
    const images = Array.from(contentRoot.querySelectorAll("img"))
      .filter(isVisible)
      .map((img) => img.src)
      .filter(Boolean);
    return {
      imageEvidence: images.length ? "yes" : "no",
      imageCount: images.length,
      imageUrls: images.slice(0, 20),
    };
  }

  function run(options) {
    const runtimeOptions = Object.assign({}, runtimePageOptions, options || {});
    const contentRoot = chooseContentRoot();
    const topCenterTitle = normalizeKnownRoomName(chooseTopCenterTitle());
    const activeLeftRoom = chooseActiveLeftRoom();
    const initialRoomAnchor = !isWeakRoomAnchor(activeLeftRoom)
      ? activeLeftRoom
      : (!isWeakRoomAnchor(topCenterTitle) ? topCenterTitle : activeLeftRoom);

    let visibleMessages = extractVisibleMessages(contentRoot, initialRoomAnchor);
    const viewOrder = detectHistoryViewOrder(contentRoot);
    const primaryMessage = choosePrimaryMessage(visibleMessages, viewOrder);
    const topicAnchor = chooseTopicAnchor(primaryMessage, initialRoomAnchor);
    let roomAnchor = inferRoomAnchorFromMessages(initialRoomAnchor, visibleMessages, topicAnchor);
    roomAnchor = normalizeKnownRoomName(roomAnchor || initialRoomAnchor || "");
    if (roomAnchor !== initialRoomAnchor) {
      visibleMessages = extractVisibleMessages(contentRoot, roomAnchor);
    }

    const finalPrimaryMessage = choosePrimaryMessage(visibleMessages, viewOrder);
    const finalTopicAnchor = chooseTopicAnchor(finalPrimaryMessage, roomAnchor);
    const imageInfo = chooseImageEvidence(contentRoot);
    const result = {
      export_version: EXPORT_VERSION,
      exported_at: new Date().toISOString(),
      page_title: document.title,
      page_url: location.href,
      source_family: "信息直播间",
      source_url: "https://mx2025.hhhuu.com/#/",
      access_mode: "login_state_required",
      sample_date: finalPrimaryMessage ? finalPrimaryMessage.display_date : "",
      room_anchor: roomAnchor || initialRoomAnchor || "",
      history_entry: "历史记录",
      display_date: finalPrimaryMessage ? finalPrimaryMessage.display_date : "",
      display_time: finalPrimaryMessage ? finalPrimaryMessage.display_time : "",
      topic_anchor: finalTopicAnchor,
      excerpt: finalPrimaryMessage ? stripSpeakerLabel(finalPrimaryMessage.text) : "",
      image_evidence: imageInfo.imageEvidence,
      image_count: imageInfo.imageCount,
      image_urls: imageInfo.imageUrls,
      visible_messages: visibleMessages,
      content_form: "static_text_and_image",
      a5_role_layer: "explanation_layer_or_side_evidence",
      notes: "",
      heuristics: {
        export_failed_reason: "",
        history_view_order: viewOrder,
        primary_pick: viewOrder === "forward" ? "earliest_visible" : "latest_visible",
        content_root_pick: {
          has_left_room_list: true,
          min_left: 150,
          picked: {
            rect: {
              top: Math.round(contentRoot.getBoundingClientRect().top),
              left: Math.round(contentRoot.getBoundingClientRect().left),
              width: Math.round(contentRoot.getBoundingClientRect().width),
              height: Math.round(contentRoot.getBoundingClientRect().height),
            },
            tag: contentRoot.tagName.toLowerCase(),
            class_name: cleanText(contentRoot.className || ""),
          },
        },
        content_text_length: getText(contentRoot).length,
        content_root_tag: contentRoot.tagName.toLowerCase(),
        first_message_candidate: finalPrimaryMessage ? stripSpeakerLabel(finalPrimaryMessage.text) : "",
        visible_message_count: visibleMessages.length,
        primary_message_candidate: finalPrimaryMessage ? stripSpeakerLabel(finalPrimaryMessage.text) : "",
        initial_room_anchor_candidate: initialRoomAnchor,
        room_anchor_candidate: roomAnchor || initialRoomAnchor || "",
        topic_anchor_candidate: finalTopicAnchor,
        forced_room_anchor: runtimeOptions.forced_room_anchor || runtimeOptions.forcedRoomAnchor || "",
        promo_strip_enabled: true,
        merged_card_split_enabled: true,
      },
    };

    if (runtimeOptions.download !== false) {
      const fileTs = new Date()
        .toISOString()
        .replace(/[-:]/g, "")
        .replace(/\..+/, "")
        .replace("T", "_");
      const filename = `info_live_export__${fileTs}.json`;
      const blob = new Blob([JSON.stringify(result, null, 2)], {
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

    window.__runInfoLiveCurrentPageExportV1 = run;
    window.__infoLiveCurrentPageExportV1 = result;
    console.log(EXPORT_VERSION, result);
    return result;
  }

  window.__runInfoLiveCurrentPageExportV1 = run;
  return run({ download: true });
})();
