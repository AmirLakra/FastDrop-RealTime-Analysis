export default function AlertPanel({ alerts }) {
  return (
    <div className="alert-panel">
      {alerts.map((alert, index) => (
        <article key={`${alert.title}-${index}`} className={`alert-card level-${alert.level}`}>
          <div className="alert-head">
            <strong>{alert.title}</strong>
            <span>{alert.level}</span>
          </div>
          <p>{alert.body}</p>
        </article>
      ))}
    </div>
  );
}

