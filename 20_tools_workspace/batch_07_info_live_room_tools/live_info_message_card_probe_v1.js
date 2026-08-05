(function () {
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
      if (/(auto|scroll|hidden|overlay)/i.test(overflowText)) {
        ancestors.push(current);
      }
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

  function cleanText(text) {
    return (text || "")
      .replace(/\u00a0/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function getText(el) {
    return cleanText(el.innerText || el.textContent || "");
  }

  function cssPath(el) {
    if (!(el instanceof Element)) return "";
    const parts = [];
    let current = el;
    while (current && current.nodeType === 1 && parts.length < 6) {
      let selector = current.tagName.toLowerCase();
      if (current.id) {
        selector += `#${current.id}`;
        parts.unshift(selector);
        break;
      }
      const className = cleanText(current.className || "")
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .join(".");
      if (className) selector += `.${className}`;
      parts.unshift(selector);
      current = current.parentElement;
    }
    return parts.join(" > ");
  }

  function isLeafLike(el) {
    const text = getText(el);
    if (!text) return false;
    const childWithSameText = Array.from(el.children).some((child) => {
      if (!isVisible(child)) return false;
      return getText(child) === text;
    });
    return !childWithSameText;
  }

  function parseDateTime(text) {
    const match = text.match(
      /(20\d{2}[\/-]\d{2}[\/-]\d{2})\s+(\d{2}:\d{2}:\d{2})/
    );
    if (!match) return null;
    return { display_date: match[1], display_time: match[2] };
  }

  function isTightTimeAnchorText(text) {
    const value = cleanText(text || "");
    if (!value) return false;
    return /^(?:讲师\s+)?20\d{2}[\/-]\d{2}[\/-]\d{2}\s+\d{2}:\d{2}:\d{2}$/.test(
      value
    );
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

  function chooseContentRoot() {
    return (
      Array.from(document.querySelectorAll("body *"))
        .filter(isVisible)
        .map((el) => ({
          el,
          rect: el.getBoundingClientRect(),
          text: getText(el),
        }))
        .filter(
          (item) =>
            item.rect.left > 180 &&
            item.rect.width > 320 &&
            item.rect.height > 140 &&
            item.text.length > 80
        )
        .sort((a, b) => b.text.length - a.text.length)[0]?.el || document.body
    );
  }

  function findMessageCardRoot(anchorEl, contentRoot) {
    const candidates = [];
    let current = anchorEl;
    while (current && current instanceof Element && current !== contentRoot) {
      const rect = current.getBoundingClientRect();
      if (rect.width > 320 && rect.height > 40 && rect.left > 20) {
        const leafEntries = getLeafEntries(current);
        const texts = leafEntries.map((entry) => entry.text);
        const timeCount = texts.filter((text) => parseDateTime(text)).length;
        const bodyCount = texts.filter((text) => !parseDateTime(text) && text.length >= 2).length;
        const className = cleanText(current.className || "");
        let score = 0;
        score += Math.min(timeCount, 3) * 20;
        score += Math.min(bodyCount, 6) * 12;
        if (/cu-card/i.test(className)) score += 80;
        if (/flex/i.test(className)) score += 10;
        if (rect.height >= 80) score += 20;
        if (rect.height >= 110) score += 10;
        if (current === contentRoot) score -= 120;
        if (bodyCount === 0) score -= 40;
        candidates.push({ el: current, score });
      }
      current = current.parentElement;
    }
    candidates.sort((a, b) => b.score - a.score);
    return candidates[0]?.el || anchorEl.parentElement || anchorEl;
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

  const contentRoot = chooseContentRoot();
  const leafEntries = getLeafEntries(contentRoot);
  const timeAnchors = leafEntries
    .filter((entry) => parseDateTime(entry.text) && isTightTimeAnchorText(entry.text))
    .sort((a, b) => a.rect.top - b.rect.top);

  const anchorSummaries = timeAnchors.slice(0, 20).map((entry) => {
    const cardRoot = findMessageCardRoot(entry.el, contentRoot);
    const rect = cardRoot.getBoundingClientRect();
    return {
      time_text: entry.text,
      time_path: cssPath(entry.el),
      time_rect: {
        top: Math.round(entry.rect.top),
        left: Math.round(entry.rect.left),
        width: Math.round(entry.rect.width),
        height: Math.round(entry.rect.height),
      },
      card_path: cssPath(cardRoot),
      card_rect: {
        top: Math.round(rect.top),
        left: Math.round(rect.left),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      },
      card_preview: getText(cardRoot).slice(0, 300),
    };
  });

  const result = {
    probe_version: "live_info_message_card_probe_v1",
    exported_at: new Date().toISOString(),
    page_title: document.title,
    page_url: location.href,
    viewport: {
      width: window.innerWidth,
      height: window.innerHeight,
    },
    content_root_path: cssPath(contentRoot),
    content_root_rect: {
      top: Math.round(contentRoot.getBoundingClientRect().top),
      left: Math.round(contentRoot.getBoundingClientRect().left),
      width: Math.round(contentRoot.getBoundingClientRect().width),
      height: Math.round(contentRoot.getBoundingClientRect().height),
    },
    visible_leaf_count: leafEntries.length,
    visible_time_anchor_count: timeAnchors.length,
    time_anchors: anchorSummaries,
  };

  const fileTs = result.exported_at
    .replace(/[-:]/g, "")
    .replace(/\..+/, "")
    .replace("T", "_");
  const filename = `info_live_message_card_probe__${fileTs}.json`;
  window.__infoLiveMessageCardProbeV1 = result;
  downloadJson(filename, result);
  console.log("info_live_message_card_probe_v1", result);
  return result;
})();
