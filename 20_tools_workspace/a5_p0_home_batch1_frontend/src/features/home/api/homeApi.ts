import {
  homeBootstrapMockDecisionRecords,
  homeBootstrapMockEvents,
} from "@/features/home/api/mock/homeBootstrapMock";
import type { DecisionRecord, EventItem } from "@/features/home/types";

export interface HomeBootstrapPayload {
  events: EventItem[];
  decisionRecords: DecisionRecord[];
}

export async function fetchHomeBootstrap(): Promise<HomeBootstrapPayload> {
  await Promise.resolve();
  return {
    events: homeBootstrapMockEvents,
    decisionRecords: homeBootstrapMockDecisionRecords,
  };
}
