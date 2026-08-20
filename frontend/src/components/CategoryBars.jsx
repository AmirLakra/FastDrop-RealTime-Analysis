export default function CategoryBars({ items, valueFormatter }) {
  const maxValue = Math.max(...items.map((item) => item.total_revenue), 1);

  return (
    <div className="category-bars">
      {items.map((item) => (
        <div key={item.category} className="category-row">
          <div className="category-meta">
            <strong>{item.category}</strong>
            <span>{valueFormatter(item.total_revenue)}</span>
          </div>
          <div className="category-track">
            <div className="category-fill" style={{ width: `${(item.total_revenue / maxValue) * 100}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

