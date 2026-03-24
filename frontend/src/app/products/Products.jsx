"use client";
import { useEffect, useState } from "react";
import Pagination from "../components/Pagination";
import CategoriesMenu from "../components/CategoriesMenu";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [category, setCategory] = useState(""); // default = all

  // Fetch products
  useEffect(() => {
    let url = `http://127.0.0.1:8000/api/products?page=${currentPage}&limit=10`;
    if (category) url += `&category=${category}`;

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setProducts(data.products);
        setTotalPages(Math.ceil(data.total / 10));
      });
  }, [currentPage, category]);

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
    <div className="p-20 flex gap-8">
      {/* Sidebar */}
      <CategoriesMenu
        selectedCategory={category}
        onSelect={(cat) => {
          setCategory(cat); // update category
          setCurrentPage(1); // reset page
        }}
      />

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
          {products.map((product) => (
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
