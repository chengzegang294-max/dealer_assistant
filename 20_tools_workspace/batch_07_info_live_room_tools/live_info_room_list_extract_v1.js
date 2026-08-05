(async function () {
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
    return rect.width > 0 && rect.height > 0;
  }

  function cleanText(text) {
    return (text || "")
      .replace(/\u00a0/g, " ")
      .replace(/\s+/g, " ")
      .trim();
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
      const parent = current.parentElement;
      if (parent) {
        const siblings = Array.from(parent.children).filter(
          (node) => node.tagName === current.tagName
        );
        if (siblings.length > 1) {
          selector += `:nth-of-type(${siblings.indexOf(current) + 1})`;
        }
      }
      parts.unshift(selector);
      current = current.parentElement;
    }
    return parts.join(" > ");
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

  function getRoleHint(el) {
    const attrs = [
      el.getAttribute("role"),
      el.getAttribute("aria-selected"),
      el.getAttribute("aria-current"),
    ]
      .filter(Boolean)
      .join("|");
    return cleanText(attrs);
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

  function dedupeVisibleCandidates(candidates) {
    const seen = new Map();
    for (const item of candidates) {
      const key = item.text;
      const current = seen.get(key);
      const score =
        item.rect.width +
        item.rect.height +
        (/active|current|selected|focus|checked|on/i.test(item.classText) ? 80 : 0);
      if (!current || score > current.score) {
        seen.set(key, { score, item });
      }
    }
    return Array.from(seen.values())
      .map((entry) => entry.item)
      .sort((a, b) => {
        if (Math.abs(a.rect.top - b.rect.top) > 6) return a.rect.top - b.rect.top;
        return a.rect.left - b.rect.left;
      });
  }

  function countRoomNodes(root) {
    if (!(root instanceof Element)) return 0;
    return root.querySelectorAll('[id^="room"]').length;
  }

  function findScrollContainerFromCandidate(candidateEl) {
    const maxLeft = Math.min(window.innerWidth * 0.4, 520);
    const visited = [];
    let current = candidateEl ? candidateEl.parentElement : null;
    while (current && current instanceof Element) {
      const rect = current.getBoundingClientRect();
      const style = window.getComputedStyle(current);
      const roomNodes = countRoomNodes(current);
      const scrollable = current.scrollHeight > current.clientHeight + 40;
      const leftish = rect.left < maxLeft;
      const overflowScrollable = /(auto|scroll|overlay)/i.test(
        `${style.overflowY} ${style.overflow}`
      );
      if (
        leftish &&
        roomNodes >= 4 &&
        rect.height >= 180 &&
        rect.width <= 420 &&
        (scrollable || overflowScrollable)
      ) {
        visited.push({
          el: current,
          rect,
          roomNodes,
          scrollable,
        });
      }
      current = current.parentElement;
    }

    visited.sort((a, b) => {
      const scoreA =
        (a.scrollable ? 100 : 0) + a.roomNodes * 5 - a.rect.width - a.rect.height;
      const scoreB =
        (b.scrollable ? 100 : 0) + b.roomNodes * 5 - b.rect.width - b.rect.height;
      return scoreB - scoreA;
    });
    return visited.length ? visited[0].el : null;
  }

  function buildRoomRecord(item, globalOrder) {
    const { el, rect, text, classText } = item;
    const roomContainer = getRoomContainer(el);
    const activeByClass = /active|current|selected|focus|checked|on/i.test(classText);
    const activeByAria =
      el.getAttribute("aria-selected") === "true" ||
      el.getAttribute("aria-current") === "true";

    const leafNodes = roomContainer
      ? Array.from(roomContainer.querySelectorAll("*"))
          .filter(isVisible)
          .filter(isLeafLike)
          .map((node) => {
            const nodeRect = node.getBoundingClientRect();
            const nodeText = cleanText(node.innerText || node.textContent || "");
            return {
              node,
              rect: nodeRect,
              text: nodeText,
              classText: cleanText(node.className || ""),
            };
          })
          .filter((entry) => entry.text)
      : [];

    const subtitleCandidates = leafNodes
      .filter((entry) => entry.text !== text)
      .filter((entry) => entry.rect.top >= rect.top - 2)
      .filter((entry) => entry.rect.left <= rect.left + 48)
      .filter((entry) => entry.rect.width >= 40)
      .filter(
        (entry) =>
          !/^20\d{2}\/\d{2}\/\d{2}$/.test(entry.text) &&
          !/^\d{2}\/\d{2}\s+\d{2}:\d{2}$/.test(entry.text) &&
          !/^\d{2}:\d{2}$/.test(entry.text)
      )
      .sort((a, b) => {
        if (Math.abs(a.rect.top - b.rect.top) > 4) return a.rect.top - b.rect.top;
        return a.rect.left - b.rect.left;
      });

    const previewText = subtitleCandidates
      .map((entry) => entry.text)
      .find((value) => value && value !== text) || "";

    const timeCandidates = leafNodes
      .map((entry) => entry.text)
      .filter((value) => /^\d{2}\/\d{2}\s+\d{2}:\d{2}$/.test(value) || /^\d{2}:\d{2}$/.test(value));

    const latestTimeText = timeCandidates[0] || "";
    const latestDateBadge = leafNodes
      .map((entry) => entry.text)
      .find((value) => /^20\d{2}\/\d{2}\/\d{2}$/.test(value)) || "";

    const rightSideHints = leafNodes
      .filter((entry) => entry.rect.left >= rect.left + rect.width + 120)
      .sort((a, b) => a.rect.left - b.rect.left)
      .slice(0, 6)
      .map((entry) => ({
        text: entry.text,
        class_name: entry.classText,
        css_path: cssPath(entry.node),
      }));

    const notificationHint = rightSideHints
      .map((entry) => `${entry.text}|${entry.class_name}`)
      .join(" || ");

    const contentFormHint = /\[图片\]|图片|img|image/i.test(previewText)
      ? "image_heavy_candidate"
      : "text_primary_candidate";

    return {
      visible_order: globalOrder,
      room_anchor: text,
      is_active: activeByClass || activeByAria,
      active_hint: activeByClass ? "class" : activeByAria ? "aria" : "",
      role_hint: getRoleHint(el),
      room_container_id: roomContainer ? roomContainer.id : "",
      latest_preview_text: previewText,
      latest_time_text: latestTimeText,
      latest_date_badge: latestDateBadge,
      content_form_hint: contentFormHint,
      notification_hint: notificationHint,
      right_side_hints: rightSideHints,
      css_path: cssPath(el),
      rect: {
        left: Math.round(rect.left),
        top: Math.round(rect.top),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      },
      class_name: classText,
    };
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

  function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function getScrollState(container) {
    if (!container) {
      return {
        top: Math.round(window.scrollY),
        maxTop: Math.max(
          0,
          Math.round(
            Math.max(
              document.documentElement.scrollHeight,
              document.body.scrollHeight
            ) - window.innerHeight
          )
        ),
      };
    }
    return {
      top: Math.round(container.scrollTop),
      maxTop: Math.max(0, Math.round(container.scrollHeight - container.clientHeight)),
    };
  }

  function scrollOneStep(container) {
    if (!container) {
      const before = getScrollState(null).top;
      const step = Math.max(280, Math.round(window.innerHeight * 0.75));
      window.scrollTo(0, before + step);
      return getScrollState(null);
    }

    const step = Math.max(220, Math.round(container.clientHeight * 0.75));
    const nextTop = Math.min(container.scrollTop + step, container.scrollHeight);
    container.scrollTop = nextTop;
    return getScrollState(container);
  }

  const initialCandidates = dedupeVisibleCandidates(getRoomTitleCandidates());
  const scrollContainer = findScrollContainerFromCandidate(
    initialCandidates[0] ? initialCandidates[0].el : null
  );

  const roomMap = new Map();
  const passSummaries = [];
  let stagnantPasses = 0;
  const maxPasses = 30;

  for (let pass = 1; pass <= maxPasses; pass += 1) {
    const beforeCount = roomMap.size;
    const visibleRooms = dedupeVisibleCandidates(getRoomTitleCandidates());
    visibleRooms.forEach((item) => {
      if (!roomMap.has(item.text)) {
        roomMap.set(item.text, buildRoomRecord(item, roomMap.size + 1));
      }
    });

    const scrollBefore = getScrollState(scrollContainer);
    const passAdded = roomMap.size - beforeCount;
    passSummaries.push({
      pass,
      visible_count: visibleRooms.length,
      added_count: passAdded,
      scroll_top: scrollBefore.top,
      scroll_max_top: scrollBefore.maxTop,
    });

    const reachedBottom = scrollBefore.top >= scrollBefore.maxTop;
    if (reachedBottom) break;

    const scrolled = scrollOneStep(scrollContainer);
    await wait(700);
    const scrollAfter = getScrollState(scrollContainer);
    const didMove = scrollAfter.top > scrollBefore.top || scrolled.top > scrollBefore.top;

    if (passAdded === 0 && !didMove) {
      stagnantPasses += 1;
    } else if (passAdded === 0) {
      stagnantPasses += 1;
    } else {
      stagnantPasses = 0;
    }

    if (stagnantPasses >= 2) break;
  }

  const rooms = Array.from(roomMap.values()).sort(
    (a, b) => a.visible_order - b.visible_order
  );

  const result = {
    export_version: "live_info_room_list_extract_v1_auto_scroll",
    exported_at: new Date().toISOString(),
    page_title: document.title,
    page_url: location.href,
    source_family: "信息直播间",
    source_url: "https://mx2025.hhhuu.com/#/",
    access_mode: "login_state_required",
    viewport: {
      width: window.innerWidth,
      height: window.innerHeight,
    },
    auto_scroll_enabled: true,
    scroll_container: scrollContainer
      ? {
          css_path: cssPath(scrollContainer),
          client_height: Math.round(scrollContainer.clientHeight),
          scroll_height: Math.round(scrollContainer.scrollHeight),
        }
      : null,
    pass_count: passSummaries.length,
    pass_summaries: passSummaries,
    room_count: rooms.length,
    rooms,
  };

  const fileTs = result.exported_at
    .replace(/[-:]/g, "")
    .replace(/\..+/, "")
    .replace("T", "_");
  const filename = `info_live_room_list__${fileTs}.json`;

  window.__infoLiveRoomListExtractV1 = result;
  downloadJson(filename, result);
  console.log("info_live_room_list_extract_v1_auto_scroll", result);
  return result;
})();
