"use client";
import React, { useState } from "react";

export default function CategoriesMenu({ selectedCategory, onSelect }) {
  const [hovered, setHovered] = useState(null);

  const categories = [
    { label: "Laptops", value: "laptop" },
    { label: "Smartphones", value: "smartphone" },
    { label: "Smartwatches", value: "smartwatch" },
  ];

  return (
    <div className="w-[286px] flex flex-col gap-4">
      <h2 className="font-inter font-semibold text-[32px]">Categories</h2>

      <div className="flex flex-col gap-3">
        {/* All Products */}
        <div
          onClick={() => onSelect("")}
          onMouseEnter={() => setHovered("")}
          onMouseLeave={() => setHovered(null)}
          className={`cursor-pointer font-inter text-[16px] ${
            selectedCategory === "" || hovered === ""
              ? "font-bold"
              : "font-medium"
          }`}
        >
          All
        </div>

        {/* Specific Categories */}
        {categories.map((cat) => (
          <div
            key={cat.value}
            onClick={() => onSelect(cat.value)}
            onMouseEnter={() => setHovered(cat.value)}
            onMouseLeave={() => setHovered(null)}
            className={`cursor-pointer font-inter text-[16px] ${
              selectedCategory === cat.value || hovered === cat.value
                ? "font-bold"
                : "font-medium"
            }`}
          >
            {cat.label}
          </div>
        ))}
      </div>
    </div>
  );
}