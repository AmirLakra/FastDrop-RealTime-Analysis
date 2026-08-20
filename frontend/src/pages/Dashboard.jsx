import { startTransition, useDeferredValue, useEffect, useState } from "react";

import AlertPanel from "../components/AlertPanel";
import CategoryBars from "../components/CategoryBars";
import DataTable from "../components/DataTable";
import DeliveryMap from "../components/DeliveryMap";
import FilterBar from "../components/FilterBar";
import KpiCard from "../components/KpiCard";
import SectionCard from "../components/SectionCard";
import TrendChart from "../components/TrendChart";
import { fetchCities, fetchDashboard } from "../services/api";
import { connectDashboardSocket } from "../services/websocket";

const statusOptions = [
  { value: "PLACED", label: "Placed" },
  { value: "ACCEPTED", label: "Accepted" },
  { value: "PICKED_UP", label: "Picked Up" },
  { value: "DELIVERED", label: "Delivered" },
  { value: "CANCELLED", label: "Cancelled" },
];

const categoryOptions = [
  { value: "Food", label: "Food" },
  { value: "Groceries", label: "Groceries" },
  { value: "Pharmacy", label: "Pharmacy" },
  { value: "Electronics", label: "Electronics" },
  { value: "Bakery", label: "Bakery" },
  { value: "Beverages", label: "Beverages" },
];

const currency = new Intl.NumberFormat("en-IN", {
  maximumFractionDigits: 0,
  style: "currency",
  currency: "INR",
});

function number(value) {
  return new Intl.NumberFormat("en-IN").format(Math.round(value ?? 0));
}

function compactCurrency(value) {
  return currency.format(value ?? 0).replace(".00", "");
}

function minutes(value) {
  return `${Number(value ?? 0).toFixed(1)} min`;
}

function percent(value) {
  return `${Number(value ?? 0).toFixed(1)}%`;
}

const emptySnapshot = {
  timestamp: new Date().toISOString(),
  kpis: {
    total_orders: 0,
    total_revenue: 0,
    average_order_value: 0,
    delivered_orders: 0,
    cancelled_orders: 0,
    cancellation_rate: 0,
    average_delivery_minutes: 0,
    average_distance: 0,
    on_time_delivery_rate: 0,
    active_agents: 0,
    orders_per_minute: 0,
    orders_last_5_minutes: 0,
    revenue_last_5_minutes: 0,
  },
  hourly_metrics: [],
  daily_metrics: [],
  delivery_metrics: [],
  revenue_by_category: [],
  top_agents: [],
  top_customers: [],
  top_products: [],
  recent_orders: [],
  locations: [],
  alerts: [],
};

export default function Dashboard() {
  const [filters, setFilters] = useState({ city: "", status: "", category: "", limit: 25 });
  const deferredFilters = useDeferredValue(filters);
  const [snapshot, setSnapshot] = useState(emptySnapshot);
  const [cities, setCities] = useState([]);
  const [connectionState, setConnectionState] = useState("connecting");
  const [loadingState, setLoadingState] = useState("loading");

  useEffect(() => {
    fetchCities()
      .then((data) => setCities(data.map((city) => ({ value: city, label: city }))))
      .catch(() => setCities([]));
  }, []);

  useEffect(() => {
    let active = true;
    setLoadingState("loading");
    fetchDashboard(deferredFilters)
      .then((data) => {
        if (!active) {
          return;
        }
        startTransition(() => {
          setSnapshot(data);
          setLoadingState("ready");
        });
      })
      .catch(() => {
        if (!active) {
          return;
        }
        setLoadingState("error");
      });
    return () => {
      active = false;
    };
  }, [deferredFilters]);

  useEffect(() => {
    return connectDashboardSocket({
      onStatusChange: setConnectionState,
      onMessage: () => {
        fetchDashboard(filters)
          .then((data) => {
            startTransition(() => {
              setSnapshot(data);
              setLoadingState("ready");
            });
          })
          .catch(() => setLoadingState("error"));
      },
    });
  }, [filters]);

  const cards = [
    {
      label: "Total Orders",
      value: number(snapshot.kpis.total_orders),
      detail: `${number(snapshot.kpis.orders_last_5_minutes)} in 5 min`,
    },
    {
      label: "Revenue",
      value: compactCurrency(snapshot.kpis.total_revenue),
      detail: compactCurrency(snapshot.kpis.revenue_last_5_minutes),
      tone: "good",
    },
    {
      label: "Average Order Value",
      value: compactCurrency(snapshot.kpis.average_order_value),
      detail: "network average",
    },
    {
      label: "Average Delivery Time",
      value: minutes(snapshot.kpis.average_delivery_minutes),
      detail: `${snapshot.kpis.average_distance.toFixed(1)} km avg`,
      tone: snapshot.kpis.average_delivery_minutes > 45 ? "warn" : "good",
    },
    {
      label: "Cancellation Rate",
      value: percent(snapshot.kpis.cancellation_rate),
      detail: `${number(snapshot.kpis.cancelled_orders)} cancelled`,
      tone: snapshot.kpis.cancellation_rate > 15 ? "warn" : "neutral",
    },
    {
      label: "On-Time Rate",
      value: percent(snapshot.kpis.on_time_delivery_rate),
      detail: `${number(snapshot.kpis.delivered_orders)} delivered`,
      tone: "good",
    },
    {
      label: "Active Agents",
      value: number(snapshot.kpis.active_agents),
      detail: connectionState,
    },
    {
      label: "Orders / Minute",
      value: number(snapshot.kpis.orders_per_minute),
      detail: `updated ${new Date(snapshot.timestamp).toLocaleTimeString()}`,
    },
  ];

  return (
    <main className="dashboard-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">QuickDrop</p>
          <h1>Real-Time Delivery Analytics</h1>
          <p className="subcopy">
            Live order demand, delivery quality, customer value, and city performance in one flat control room.
          </p>
        </div>
        <div className="topbar-meta">
          <span className={`live-dot state-${connectionState}`} />
          <span>{connectionState}</span>
          <span className="timestamp">
            {loadingState === "loading" ? "Refreshing…" : new Date(snapshot.timestamp).toLocaleString()}
          </span>
        </div>
      </header>

      <FilterBar
        filters={filters}
        options={{ cities, statuses: statusOptions, categories: categoryOptions }}
        onChange={(key, value) => setFilters((current) => ({ ...current, [key]: value }))}
        onReset={() => setFilters({ city: "", status: "", category: "", limit: 25 })}
      />

      <section className="kpi-grid">
        {cards.map((item) => (
          <KpiCard key={item.label} {...item} />
        ))}
      </section>

      <section className="dashboard-grid">
        <SectionCard title="Orders Over Time" eyebrow="Demand">
          <TrendChart
            title="Hourly orders"
            points={snapshot.hourly_metrics}
            valueKey="orders"
            valueFormatter={(value) => `${number(value)} orders`}
          />
        </SectionCard>

        <SectionCard title="Revenue Momentum" eyebrow="Business">
          <TrendChart
            title="Daily revenue"
            points={snapshot.daily_metrics}
            valueKey="revenue"
            valueFormatter={compactCurrency}
            tone="green"
          />
        </SectionCard>

        <SectionCard title="Delivery Performance" eyebrow="Operations">
          <TrendChart
            title="Delivery minutes"
            points={snapshot.hourly_metrics}
            valueKey="average_delivery_minutes"
            valueFormatter={minutes}
            tone="amber"
          />
        </SectionCard>

        <SectionCard title="Revenue by Category" eyebrow="Mix">
          <CategoryBars items={snapshot.revenue_by_category} valueFormatter={compactCurrency} />
        </SectionCard>

        <SectionCard title="Recent Orders" eyebrow="Live feed">
          <DataTable
            columns={[
              { key: "order_id", label: "Order" },
              { key: "city", label: "City" },
              { key: "order_status", label: "Status" },
              { key: "total_amount", label: "Value", render: (row) => compactCurrency(row.total_amount) },
            ]}
            rows={snapshot.recent_orders}
            emptyMessage="No orders match the current filters."
          />
        </SectionCard>

        <SectionCard title="Top Agents" eyebrow="Leaderboard">
          <DataTable
            columns={[
              { key: "agent_name", label: "Agent" },
              { key: "city", label: "City" },
              { key: "deliveries", label: "Deliveries" },
              { key: "rating", label: "Rating" },
            ]}
            rows={snapshot.top_agents}
          />
        </SectionCard>

        <SectionCard title="Top Customers" eyebrow="Retention">
          <DataTable
            columns={[
              { key: "customer_name", label: "Customer" },
              { key: "city", label: "City" },
              { key: "total_orders", label: "Orders" },
              { key: "total_revenue", label: "Revenue", render: (row) => compactCurrency(row.total_revenue) },
            ]}
            rows={snapshot.top_customers}
          />
        </SectionCard>

        <SectionCard title="Top Products" eyebrow="Basket">
          <DataTable
            columns={[
              { key: "product_name", label: "Product" },
              { key: "category", label: "Category" },
              { key: "quantity_sold", label: "Units" },
              { key: "total_revenue", label: "Revenue", render: (row) => compactCurrency(row.total_revenue) },
            ]}
            rows={snapshot.top_products}
          />
        </SectionCard>

        <SectionCard title="Delivery Map" eyebrow="Geography">
          <DeliveryMap locations={snapshot.locations} />
        </SectionCard>

        <SectionCard title="Alerts" eyebrow="Monitoring">
          <AlertPanel alerts={snapshot.alerts} />
        </SectionCard>
      </section>
    </main>
  );
}

