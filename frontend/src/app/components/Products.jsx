"use client";
import { useEffect, useState } from "react";
import Pagination from "../components/Pagination";
import CategoriesMenu from "../components/CategoriesMenu";
import FilterMenu from "../components/FilterMenu";


export default function Products() {
  const [products, setProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [category, setCategory] = useState(""); // default = all
  const [activeFilters, setActiveFilters] = useState({});
  const [filterOptions, setFilterOptions] = useState({});
  const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

  // Fetch products
  useEffect(() => {
    let url = `${BASE_URL}/products?page=${currentPage}&limit=10`;
        if (category) url += `&category=${category}`;

    Object.entries(activeFilters).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        value.forEach((v) => url += `&${key}=${encodeURIComponent(v)}`);
      } else if (value !== "" && value !== null) {
        url += `&${key}=${encodeURIComponent(value)}`;
      }
    });

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setProducts(data.products);
        setTotalPages(Math.ceil(data.total / 10));
      });
  }, [currentPage, category, activeFilters]);

  // Fetch filters
  useEffect(() => {
    let url = `${BASE_URL}/filters`;
    if (category) url += `?category=${category}`;
    fetch(url).then(r => r.json()).then(setFilterOptions);
  }, [category]);

// Map category DB value to display title
const categoryTitleMap = {
  "": "",               // No title for All
  laptop: "Laptops",
  smartphone: "Smartphones",
  smartwatch: "Smartwatches",
};

const title = categoryTitleMap[category] || "";

// In JSX
{title && (
  <h1
    className="font-inter font-bold"
    style={{
      fontSize: "64px",
      marginBottom: "44px",
    }}
  >
    {title}
  </h1>
)}

  return (
    <div className="px-20 pt-10 pb-20 flex gap-8">
    {/* Sidebar */}
    <div className="flex flex-col gap-6 w-[220px] shrink-0">
      <CategoriesMenu
        selectedCategory={category}
        onSelect={(cat) => {
          setCategory(cat);
          setCurrentPage(1);
          setActiveFilters({});
        }}
      />
    <div>
      <div className="font-inter font-semibold" style={{ fontSize: "32px", marginBottom: "16px" }}>
        Filters
      </div>
      <FilterMenu
        category={category}
        filterOptions={filterOptions}
        activeFilters={activeFilters}
        onFilterChange={(newFilters) => {
          setActiveFilters(newFilters);
          setCurrentPage(1);
        }}
      />
    </div>
  </div>


      {/* Products Section */}
      <div className="flex-1">
        {/* Category Title */}
        <h1
          className="font-inter font-bold"
          style={{
            fontSize: "64px",
            marginBottom: "44px", // space between title and grid
          }}
        >
          {title}
        </h1>

        {/* Products Grid */}
        <div className="grid gap-8 [grid-template-columns:repeat(auto-fill,minmax(280px,1fr))]">
          {products?.map((product) => (
            <div key={product.id} className="bg-white">
              <div className="w-full h-[180px] bg-gray-200 rounded-[8px]" />
              <div className="pt-4 pb-2">
                <div
                  style={{
                    fontFamily: "var(--font-roboto)",
                    fontSize: "16px",
                    fontWeight: 500,
                  }}
                >
                  {product.brand} {product.model}
                </div>
                <div
                  style={{
                    fontFamily: "var(--font-inter)",
                    fontSize: "13px",
                    color: "#9CA3AF",
                  }}
                >
                  {product.description}
                </div>
                <div
                  className="mt-2"
                  style={{
                    fontFamily: "var(--font-inter)",
                    fontSize: "14px",
                    fontWeight: 500,
                  }}
                >
                  ${product.price}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Pagination */}
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
        />
      </div>
    </div>
  );
}
