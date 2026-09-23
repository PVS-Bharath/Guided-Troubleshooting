// src/types.ts – shared TypeScript types for the Troubleshooter app
export interface ActionStep {
  actionName: string;
  description: string;
  steps: string[];
  deeplink?: string;
  category?: string;
}

export interface TroubleshootResponse {
  request_id: string;
  query: string;
  goal: string;
  actions: ActionStep[];
}
