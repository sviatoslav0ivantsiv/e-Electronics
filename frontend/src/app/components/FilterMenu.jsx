"use client";

const RANGE_FILTERS = {
  laptop: ["screen_size", "weight"],
  smartphone: ["display_size", "battery_capacity"],
  smartwatch: ["battery_life"],
  "": [],
};

const RANGE_LABELS = {
  display_size: "Display Size (inches)",
  battery_capacity: "Battery Capacity (mAh)",
  screen_size: "Screen Size (inches)",
  weight: "Weight (g)",
  battery_life: "Battery Life (hrs)",
};

export default function FilterMenu({ category, filterOptions, activeFilters, onFilterChange }) {
  const rangeFields = RANGE_FILTERS[category] || [];

  function handleCheckbox(field, value) {
    const current = activeFilters[field] || [];
    const updated = current.includes(value)
      ? current.filter((v) => v !== value)
      : [...current, value];
    onFilterChange({ ...activeFilters, [field]: updated });
  }

  function handleRange(field, bound, value) {
    onFilterChange({ ...activeFilters, [`${bound}_${field}`]: value });
  }

  function handleModel(value) {
    onFilterChange({ ...activeFilters, model: value });
  }

  return (
    <div className="flex flex-col gap-6 w-[220px] shrink-0">
      {/* Always visible */}
      <div>
        <div className="font-semibold mb-2">Brand</div>
        {(filterOptions.brand || []).map((b) => (
          <label key={b} className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={(activeFilters.brand || []).includes(b)}
              onChange={() => handleCheckbox("brand", b)}
            />
            {b}
          </label>
        ))}
      </div>

      <div>
        <div className="font-semibold mb-2">Price</div>
        <div className="flex gap-2">
          <input type="number" placeholder="Min" className="border rounded p-1 w-24 text-sm"
            value={activeFilters.min_price || ""}
            onChange={(e) => onFilterChange({ ...activeFilters, min_price: e.target.value })} />
          <input type="number" placeholder="Max" className="border rounded p-1 w-24 text-sm"
            value={activeFilters.max_price || ""}
            onChange={(e) => onFilterChange({ ...activeFilters, max_price: e.target.value })} />
        </div>
      </div>

      <div>
        <div className="font-semibold mb-2">Model</div>
        <input type="text" placeholder="Search model..." className="border rounded p-1 w-full text-sm"
          value={activeFilters.model || ""}
          onChange={(e) => handleModel(e.target.value)} />
      </div>

      {/* Checkbox filters by category */}
      {["camera_mp", "cpu", "gpu", "screen_type", "water_resistance","ram", "storage"].map((field) =>
        filterOptions[field]?.length ? (
          <div key={field}>
            <div className="font-semibold mb-2 capitalize">{field.replace("_", " ")}</div>
            {filterOptions[field].map((v) => (
              <label key={v} className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={(activeFilters[field] || []).includes(v)}
                  onChange={() => handleCheckbox(field, v)}
                />
                {v}
              </label>
            ))}
          </div>
        ) : null
      )}

      {/* Range filters */}
      {rangeFields.map((field) => (
        <div key={field}>
          <div className="font-semibold mb-2">{RANGE_LABELS[field]}</div>
          <div className="flex gap-2">
            <input type="number" placeholder="Min" className="border rounded p-1 w-24 text-sm"
              value={activeFilters[`min_${field}`] || ""}
              onChange={(e) => handleRange(field, "min", e.target.value)} />
            <input type="number" placeholder="Max" className="border rounded p-1 w-24 text-sm"
              value={activeFilters[`max_${field}`] || ""}
              onChange={(e) => handleRange(field, "max", e.target.value)} />
          </div>
        </div>
      ))}
    </div>
  );
}