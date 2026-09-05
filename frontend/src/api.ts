import type { CreateItemPayload, Dashboard, InventoryItem } from "./types";

const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${apiUrl}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    throw new Error("No fue posible completar la solicitud.");
  }
  return response.json() as Promise<T>;
}

export const api = {
  getDashboard: () => request<Dashboard>("/dashboard"),
  getItems: (search = "") => request<InventoryItem[]>(`/inventory?search=${encodeURIComponent(search)}`),
  createItem: (payload: CreateItemPayload) =>
    request<InventoryItem>("/inventory", { method: "POST", body: JSON.stringify(payload) }),
  archiveItem: (id: number) => request<InventoryItem>(`/inventory/${id}/archive`, { method: "POST" }),
};
