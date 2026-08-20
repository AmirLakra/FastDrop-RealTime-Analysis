const defaultOption = { value: "", label: "All" };

function SelectField({ label, value, options, onChange }) {
  return (
    <label className="filter-field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {[defaultOption, ...options].map((option) => (
          <option key={option.value || "all"} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

export default function FilterBar({ filters, options, onChange, onReset }) {
  return (
    <section className="filter-bar">
      <div className="filter-copy">
        <p className="eyebrow">Filters</p>
        <h2>Focus the live network view</h2>
      </div>
      <div className="filter-grid">
        <SelectField
          label="City"
          value={filters.city}
          options={options.cities}
          onChange={(value) => onChange("city", value)}
        />
        <SelectField
          label="Status"
          value={filters.status}
          options={options.statuses}
          onChange={(value) => onChange("status", value)}
        />
        <SelectField
          label="Category"
          value={filters.category}
          options={options.categories}
          onChange={(value) => onChange("category", value)}
        />
        <button type="button" className="filter-reset" onClick={onReset}>
          Clear filters
        </button>
      </div>
    </section>
  );
}

