"use client";

import Slider from "rc-slider";
import "rc-slider/assets/index.css";
import { useState } from "react";



const FIELD_LABELS = {
  brand: "Brand",
  camera_mp: "Camera (MP)",
  screen_type: "Screen Type",
  water_resistance: "Water Resistance",
  ram: "RAM",
  storage: "Storage",
  cpu: "CPU",
  gpu: "GPU",
};

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
  weight: "Weight (kg)",
  battery_life: "Battery Life (hrs)",
};

function getMax(field) {
  const maxMap = {
    screen_size: 20,
    display_size: 10,
    weight: 5,
    battery_life: 100,
    battery_capacity: 10000,
  };
  return maxMap[field] || 100;
}

export default function FilterMenu({ category, filterOptions, activeFilters, onFilterChange }) {
  const rangeFields = RANGE_FILTERS[category] || [];
  const [openSections, setOpenSections] = useState({});

  function toggleSection(field) {
    setOpenSections(prev => ({ ...prev, [field]: !prev[field] }));
    }

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
    <div className="flex flex-col gap-4 w-[220px] shrink-0">
      {/* Always visible */}


      <div>
        <div className="font-regular mb-1">Price</div>
        <div className="flex gap-2 mb-1">
          <input type="number" placeholder="Min" className="border rounded p-1 w-full text-sm"
            value={activeFilters.min_price || ""}
            onChange={(e) => onFilterChange({ ...activeFilters, min_price: e.target.value })} />
          <input type="number" placeholder="Max" className="border rounded p-1 w-full text-sm"
            value={activeFilters.max_price || ""}
            onChange={(e) => onFilterChange({ ...activeFilters, max_price: e.target.value })} />
        </div>
        <Slider range
          min={0} max={5000}
          value={[activeFilters.min_price || 0, activeFilters.max_price || 5000]}
          onChange={([min, max]) => onFilterChange({ ...activeFilters, min_price: min, max_price: max })}
          styles={{
            track: { backgroundColor: "#E6E6E6", height: 8, borderRadius: 4, marginTop: 0  },
            rail: { backgroundColor: "#E6E6E6", height: 8, borderRadius: 4, marginTop: 0 },
            handle: {
              backgroundColor: "#000",
              border: "none",
              width: 16,
              height: 16,
              opacity: 1,
              boxShadow: "none",
            },
          }}
          style={{ width: "calc(100% - 16px)", margin: "0 8px" }}
        />
      </div>

      <div>
        <div className="font-regular mb-1">Model</div>
        <input type="text" placeholder="Search model..." className="border rounded p-1 w-full text-sm"
          value={activeFilters.model || ""}
          onChange={(e) => handleModel(e.target.value)} />
      </div>

      {/* Checkbox filters by category */}
      {["brand", "ram", "storage", "cpu", "gpu", "camera_mp", "screen_type", "water_resistance"].map((field) =>
        filterOptions[field]?.length ? (
          <div key={field}>
            <div
              className="flex justify-between items-center cursor-pointer mb-1"
              onClick={() => toggleSection(field)}
            >
            <div className="font-regular capitalize">
              {FIELD_LABELS[field] || field.replace(/_/g, " ")}
            </div>
              <span style={{ color: "#E6E6E6" }}>
                {openSections[field] ? "▼" : "▶"}
              </span>
            </div>
            {openSections[field] && (
            <div>
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
            )}
          </div>
        ) : null
      )}

      {/* Range filters */}
      {rangeFields.map((field) => (
          <div key={field}>
            <div className="font-regular mb-1">{RANGE_LABELS[field]}</div>
            <div className="flex gap-2 mb-1">
              <input type="number" placeholder="Min" className="border rounded p-1 w-full text-sm"
                value={activeFilters[`min_${field}`] || ""}
                onChange={(e) => handleRange(field, "min", e.target.value)} />
              <input type="number" placeholder="Max" className="border rounded p-1 w-full text-sm"
                value={activeFilters[`max_${field}`] || ""}
                onChange={(e) => handleRange(field, "max", e.target.value)} />
            </div>



            <Slider range
              min={0}
              max={getMax(field)}
              value={[activeFilters[`min_${field}`] || 0, activeFilters[`max_${field}`] || getMax(field)]}
              onChange={([min, max]) => onFilterChange({ ...activeFilters, [`min_${field}`]: min, [`max_${field}`]: max })}
              styles={{
                track: { backgroundColor: "#E6E6E6", height: 8, borderRadius: 4, marginTop: 0  },
                rail: { backgroundColor: "#E6E6E6", height: 8, borderRadius: 4, marginTop: 0 },
                handle: {
                  backgroundColor: "#000",
                  border: "none",
                  width: 16,
                  height: 16,
                  opacity: 1,
                  boxShadow: "none",
                },
              }}
              style={{ width: "calc(100% - 16px)", margin: "0 8px" }}
            />
          </div>

      ))}
    </div>
  );
}