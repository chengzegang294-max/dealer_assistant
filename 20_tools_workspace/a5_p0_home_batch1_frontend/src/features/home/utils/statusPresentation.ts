import type { ProcessStatus } from "@/features/home/types";

export function statusLabel(status: ProcessStatus) {
  if (status === "done") {
    return "已处理";
  }

  return "未处理";
}

export function statusTone(status: ProcessStatus) {
  if (status === "done") {
    return "bg-emerald-500/15 text-emerald-300 ring-1 ring-emerald-400/30";
  }

  return "bg-amber-500/15 text-amber-200 ring-1 ring-amber-300/30";
}
