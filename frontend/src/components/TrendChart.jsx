function buildPath(points, valueKey, width, height, padding) {
  const values = points.map((point) => point[valueKey] ?? 0);
  const max = Math.max(...values, 1);
  const step = points.length > 1 ? (width - padding * 2) / (points.length - 1) : 0;

  return points
    .map((point, index) => {
      const x = padding + index * step;
      const value = point[valueKey] ?? 0;
      const y = height - padding - (value / max) * (height - padding * 2);
      return `${index === 0 ? "M" : "L"} ${x} ${y}`;
    })
    .join(" ");
}

export default function TrendChart({ title, points, valueKey, valueFormatter, tone = "blue" }) {
  const width = 520;
  const height = 220;
  const padding = 20;
  const path = buildPath(points, valueKey, width, height, padding);
  const latestPoint = points.at(-1);

  return (
    <div className="chart-panel">
      <div className="chart-header">
        <h3>{title}</h3>
        <strong>{latestPoint ? valueFormatter(latestPoint[valueKey] ?? 0) : valueFormatter(0)}</strong>
      </div>
      <svg viewBox={`0 0 ${width} ${height}`} className={`trend-chart tone-${tone}`} role="img" aria-label={title}>
        <path d={path} fill="none" strokeWidth="3" />
        {points.map((point, index) => {
          const values = points.map((entry) => entry[valueKey] ?? 0);
          const max = Math.max(...values, 1);
          const step = points.length > 1 ? (width - padding * 2) / (points.length - 1) : 0;
          const x = padding + index * step;
          const y = height - padding - ((point[valueKey] ?? 0) / max) * (height - padding * 2);
          return <circle key={`${point.label}-${index}`} cx={x} cy={y} r="4" />;
        })}
      </svg>
      <div className="chart-labels">
        {points.slice(-6).map((point) => (
          <span key={point.label}>{point.label}</span>
        ))}
      </div>
    </div>
  );
}

