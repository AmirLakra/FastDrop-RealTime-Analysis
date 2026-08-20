export default function KpiCard({ label, value, detail, tone = "neutral" }) {
  return (
    <article className={`kpi-card tone-${tone}`}>
      <p className="kpi-label">{label}</p>
      <div className="kpi-value-row">
        <h3 className="kpi-value">{value}</h3>
        <span className="kpi-pill">{detail}</span>
      </div>
    </article>
  );
}

