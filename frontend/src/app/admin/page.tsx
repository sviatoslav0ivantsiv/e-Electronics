"use client";
import { useState, useEffect } from "react";

export default function AdminPage() {
  const [form, setForm] = useState({
    category: "",
    brand: "",
    model: "",
    price: "",
    stock: ""
  });

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (field, value) => {
    setForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // 🔥 ВИПРАВЛЕНИЙ fetch
  const fetchProducts = async () => {
    try {
      const res = await fetch("http://192.168.1.7:8000/api/products");
      const data = await res.json();

      console.log("DATA:", data);

      // ✅ ГОЛОВНИЙ ФІКС
      setProducts(data.products || []);
    } catch (err) {
      console.error(err);
      setProducts([]); // щоб не падало
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleSubmit = async () => {
    setLoading(true);

    try {
      const res = await fetch("http://192.168.1.7:8000/api/admin/products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          category: form.category.toLowerCase(),
          brand: form.brand,
          model: form.model,
          price: Number(form.price),
          stock: Number(form.stock),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Error");
        return;
      }

      alert("Created!");

      setForm({
        category: "",
        brand: "",
        model: "",
        price: "",
        stock: ""
      });

      fetchProducts(); // 🔄 оновити список
    } catch (err) {
      console.error(err);
      alert("Fetch error");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete product?")) return;

    try {
      await fetch(`http://192.168.1.7:8000/api/admin/products/${id}`, {
        method: "DELETE",
      });

      fetchProducts();
    } catch (err) {
      console.error(err);
    }
  };

  const handleEdit = async (product) => {
    const newPrice = prompt("New price:", product.price);
    if (!newPrice) return;

    try {
      await fetch(`http://192.168.1.7:8000/api/admin/products/${product.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          price: Number(newPrice),
        }),
      });

      fetchProducts();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Admin Panel</h1>

      {/* 🔹 Форма */}
      <div>
        <input placeholder="Category" value={form.category} onChange={e => handleChange("category", e.target.value)} />
        <input placeholder="Brand" value={form.brand} onChange={e => handleChange("brand", e.target.value)} />
        <input placeholder="Model" value={form.model} onChange={e => handleChange("model", e.target.value)} />
        <input type="number" placeholder="Price" value={form.price} onChange={e => handleChange("price", e.target.value)} />
        <input type="number" placeholder="Stock" value={form.stock} onChange={e => handleChange("stock", e.target.value)} />

        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "Creating..." : "Create Product"}
        </button>
      </div>

      {/* 🔹 Таблиця */}
      <h2>Products</h2>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Category</th>
            <th>Brand</th>
            <th>Model</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {/* 🔥 ЗАХИСТ ВІД ПОМИЛКИ */}
          {Array.isArray(products) && products.length > 0 ? (
            products.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.category}</td>
                <td>{p.brand}</td>
                <td>{p.model}</td>
                <td>{p.price}</td>
                <td>{p.stock}</td>
                <td>
                  <button onClick={() => handleEdit(p)}>Edit</button>
                  <button onClick={() => handleDelete(p.id)}>Delete</button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="7">No products</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
