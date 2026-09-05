export type ItemStatus = "active" | "archived";

export interface InventoryItem {
  id: number;
  name: string;
  category: string | null;
  description: string | null;
  quantity: number;
  location: string | null;
  image_url: string | null;
  status: ItemStatus;
  created_at: string;
  updated_at: string;
}

export interface Dashboard {
  total_items: number;
  active_items: number;
  archived_items: number;
  total_units: number;
  recent_events: Array<{
    id: number;
    item_id: number;
    action: string;
    detail: string | null;
    created_at: string;
  }>;
}

export interface CreateItemPayload {
  name: string;
  category?: string;
  quantity: number;
  location?: string;
  description?: string;
}
