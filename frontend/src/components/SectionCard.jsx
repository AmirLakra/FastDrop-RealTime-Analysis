export default function SectionCard({ title, eyebrow, children }) {
  return (
    <section className="section-card">
      <div className="section-heading">
        <p className="section-eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
      </div>
      {children}
    </section>
  );
}

