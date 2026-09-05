import { FormEvent, useEffect, useState } from "react";

import { api } from "./api";
import type { Dashboard, InventoryItem } from "./types";

const emptyDashboard: Dashboard = {
  total_items: 0,
  active_items: 0,
  archived_items: 0,
  total_units: 0,
  recent_events: [],
};

export default function App() {
  const [dashboard, setDashboard] = useState<Dashboard>(emptyDashboard);
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  const load = async (term = search) => {
    try {
      setError("");
      const [nextDashboard, nextItems] = await Promise.all([api.getDashboard(), api.getItems(term)]);
      setDashboard(nextDashboard);
      setItems(nextItems);
    } catch {
      setError("No se pudo conectar con la API. Verifica que el backend esté ejecutándose.");
    }
  };

  useEffect(() => {
    void load("");
  }, []);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setIsSaving(true);
    try {
      await api.createItem({
        name: String(form.get("name") ?? ""),
        category: String(form.get("category") ?? "") || undefined,
        location: String(form.get("location") ?? "") || undefined,
        quantity: Number(form.get("quantity") ?? 1),
        description: String(form.get("description") ?? "") || undefined,
      });
      event.currentTarget.reset();
      await load("");
    } catch {
      setError("No se pudo guardar el objeto.");
    } finally {
      setIsSaving(false);
    }
  };

  const archive = async (id: number) => {
    try {
      await api.archiveItem(id);
      await load();
    } catch {
      setError("No se pudo archivar el objeto.");
    }
  };

  return (
    <main className="shell">
      <header className="hero">
        <div>
          <p className="eyebrow">VisionBots</p>
          <h1>Tu inventario, bajo control.</h1>
          <p className="subtitle">Registra objetos hoy. Mañana, la IA te ayudará a reconocerlos.</p>
        </div>
        <button className="secondary" onClick={() => void load()} type="button">
          Actualizar
        </button>
      </header>

      {error && <p className="error">{error}</p>}

      <section className="metrics" aria-label="Resumen de inventario">
        <Metric label="Objetos" value={dashboard.total_items} />
        <Metric label="Activos" value={dashboard.active_items} />
        <Metric label="Unidades" value={dashboard.total_units} />
        <Metric label="Archivados" value={dashboard.archived_items} />
      </section>

      <section className="workspace">
        <form className="card form" onSubmit={handleSubmit}>
          <div>
            <p className="eyebrow">Registro manual</p>
            <h2>Añadir objeto</h2>
          </div>
          <label>
            Nombre
            <input name="name" placeholder="Ej. Gafas de sol" required />
          </label>
          <div className="two-columns">
            <label>
              Categoría
              <input name="category" placeholder="Accesorios" />
            </label>
            <label>
              Cantidad
              <input defaultValue="1" min="0" name="quantity" type="number" />
            </label>
          </div>
          <label>
            Ubicación
            <input name="location" placeholder="Caja principal" />
          </label>
          <label>
            Descripción
            <textarea name="description" placeholder="Detalles que ayuden a identificarlo" rows={3} />
          </label>
          <button disabled={isSaving} type="submit">
            {isSaving ? "Guardando…" : "Guardar objeto"}
          </button>
        </form>

        <section className="card inventory">
          <div className="inventory-heading">
            <div>
              <p className="eyebrow">Inventario</p>
              <h2>Objetos registrados</h2>
            </div>
            <form
              onSubmit={(event) => {
                event.preventDefault();
                void load();
              }}
            >
              <input
                aria-label="Buscar objetos"
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Buscar"
                value={search}
              />
            </form>
          </div>
          <div className="items">
            {items.length === 0 ? (
              <p className="empty">Aún no hay objetos. Crea el primero desde el formulario.</p>
            ) : (
              items.map((item) => (
                <article className="item" key={item.id}>
                  <div>
                    <h3>{item.name}</h3>
                    <p>
                      {item.category ?? "Sin categoría"} · {item.location ?? "Sin ubicación"} · {item.quantity} uds.
                    </p>
                  </div>
                  {item.status === "active" ? (
                    <button className="text-button" onClick={() => void archive(item.id)} type="button">
                      Archivar
                    </button>
                  ) : (
                    <span className="badge">Archivado</span>
                  )}
                </article>
              ))
            )}
          </div>
        </section>
      </section>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <article className="metric card">
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}
