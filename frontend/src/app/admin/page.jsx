"use client";
import { useState, useEffect } from "react";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const styles = {
  wrap: { padding: "2rem", maxWidth: 1100, margin: "0 auto", fontFamily: "sans-serif" },
  h1: { fontSize: 22, fontWeight: 500, marginBottom: "1.5rem" },
  h2: { fontSize: 18, fontWeight: 500, margin: "1.5rem 0 1rem" },
  card: { background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 12, padding: "1.25rem" },
  formGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: 12, marginBottom: "1rem" },
  input: { width: "100%", height: 36, padding: "0 12px", border: "0.5px solid #ccc", borderRadius: 8, fontSize: 14, outline: "none" },
  btn: { height: 36, padding: "0 16px", border: "0.5px solid #ccc", borderRadius: 8, fontSize: 14, background: "transparent", cursor: "pointer" },
  btnPrimary: { background: "#e8f1fb", color: "#185fa5", border: "0.5px solid #b5d4f4", borderRadius: 8, height: 36, padding: "0 16px", fontSize: 14, cursor: "pointer" },
  btnDanger: { background: "#fcebeb", color: "#a32d2d", border: "0.5px solid #f7c1c1", borderRadius: 8, height: 36, padding: "0 16px", fontSize: 14, cursor: "pointer" },
  table: { width: "100%", borderCollapse: "collapse", fontSize: 14 },
  th: { textAlign: "left", padding: "10px 12px", fontWeight: 500, fontSize: 13, color: "#888", borderBottom: "0.5px solid #e0e0e0" },
  td: { padding: "10px 12px", borderBottom: "0.5px solid #f0f0f0" },
  badge: { display: "inline-block", padding: "2px 8px", borderRadius: 6, fontSize: 12, background: "#e8f1fb", color: "#185fa5" },
  overlay: { position: "fixed", inset: 0, background: "rgba(0,0,0,0.4)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100 },
  modal: { background: "#fff", borderRadius: 12, padding: "1.5rem", width: 400, border: "0.5px solid #e0e0e0" },
};

const EMPTY_FORM = { category: "", brand: "", model: "", price: "", stock: "" };

export default function AdminPage() {
  const [form, setForm] = useState(EMPTY_FORM);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editProduct, setEditProduct] = useState(null);

  const getToken = () => localStorage.getItem("token");
  const authHeaders = () => ({
    "Content-Type": "application/json",
    "Authorization": `Bearer ${getToken()}`
  });

  const fetchProducts = async () => {
    try {
      const res = await fetch(`${BASE_URL}/products?limit=100`);
      const data = await res.json();
      setProducts(data.products || []);
    } catch (err) {
      console.error(err);
      setProducts([]);
    }
  };

  useEffect(() => { fetchProducts(); }, []);

  const handleChange = (field, value) => setForm(prev => ({ ...prev, [field]: value }));

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/products`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({
          category: form.category.toLowerCase(),
          brand: form.brand,
          model: form.model,
          price: Number(form.price),
          stock: Number(form.stock),
        }),
      });
      const data = await res.json();
      if (!res.ok) { alert(data.detail || "Error"); return; }
      setForm(EMPTY_FORM);
      fetchProducts();
    } catch (err) {
      alert("Fetch error");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete product?")) return;
    try {
      await fetch(`${BASE_URL}/products/${id}`, {
        method: "DELETE",
        headers: authHeaders(),
      });
      fetchProducts();
    } catch (err) { console.error(err); }
  };

  const handleEditSave = async () => {
    try {
      await fetch(`${BASE_URL}/products/${editProduct.id}`, {
        method: "PATCH",
        headers: authHeaders(),
        body: JSON.stringify({
          category: editProduct.category,
          brand: editProduct.brand,
          model: editProduct.model,
          price: Number(editProduct.price),
          stock: Number(editProduct.stock),
        }),
      });
      setEditProduct(null);
      fetchProducts();
    } catch (err) { console.error(err); }
  };

  return (
    <div style={styles.wrap}>
      <h1 style={styles.h1}>Admin panel</h1>

      <div style={styles.card}>
        <h2 style={{ ...styles.h2, marginTop: 0 }}>Add product</h2>
        <div style={styles.formGrid}>
          {["category", "brand", "model"].map(f => (
            <input key={f} style={styles.input} placeholder={f.charAt(0).toUpperCase() + f.slice(1)}
              value={form[f]} onChange={e => handleChange(f, e.target.value)} />
          ))}
          <input style={styles.input} type="number" placeholder="Price"
            value={form.price} onChange={e => handleChange("price", e.target.value)} />
          <input style={styles.input} type="number" placeholder="Stock"
            value={form.stock} onChange={e => handleChange("stock", e.target.value)} />
        </div>
        <button style={styles.btnPrimary} onClick={handleSubmit} disabled={loading}>
          {loading ? "Creating..." : "Create product"}
        </button>
      </div>

      <h2 style={styles.h2}>Products</h2>
      <div style={{ ...styles.card, padding: 0, overflow: "hidden" }}>
        <table style={styles.table}>
          <thead>
            <tr>
              {["ID", "Category", "Brand", "Model", "Price", "Stock", "Actions"].map(h => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {products.length > 0 ? products.map(p => (
              <tr key={p.id}>
                <td style={styles.td}>{p.id}</td>
                <td style={styles.td}><span style={styles.badge}>{p.category}</span></td>
                <td style={styles.td}>{p.brand}</td>
                <td style={styles.td}>{p.model}</td>
                <td style={styles.td}>${p.price}</td>
                <td style={styles.td}>{p.stock}</td>
                <td style={styles.td}>
                  <div style={{ display: "flex", gap: 8 }}>
                    <button style={styles.btn} onClick={() => setEditProduct({ ...p })}>Edit</button>
                    <button style={styles.btnDanger} onClick={() => handleDelete(p.id)}>Delete</button>
                  </div>
                </td>
              </tr>
            )) : (
              <tr><td style={styles.td} colSpan={7}>No products</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {editProduct && (
        <div style={styles.overlay}>
          <div style={styles.modal}>
            <h2 style={{ ...styles.h2, marginTop: 0 }}>Edit product</h2>
            {["category", "brand", "model", "price", "stock"].map(f => (
              <input key={f} style={{ ...styles.input, marginBottom: 10 }}
                placeholder={f.charAt(0).toUpperCase() + f.slice(1)}
                type={["price", "stock"].includes(f) ? "number" : "text"}
                value={editProduct[f]}
                onChange={e => setEditProduct(prev => ({ ...prev, [f]: e.target.value }))} />
            ))}
            <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
              <button style={styles.btnPrimary} onClick={handleEditSave}>Save</button>
              <button style={styles.btn} onClick={() => setEditProduct(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
// "use client";
// import { useState, useEffect } from "react";

// const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// export default function AdminPage() {
//   const [form, setForm] = useState({
//     category: "",
//     brand: "",
//     model: "",
//     price: "",
//     stock: ""
//   });

//   const [products, setProducts] = useState([]);
//   const [loading, setLoading] = useState(false);

//   const getToken = () => localStorage.getItem("token");

//   const authHeaders = () => ({
//     "Content-Type": "application/json",
//     "Authorization": `Bearer ${getToken()}`
//   });

//   const fetchProducts = async () => {
//     try {
//       const res = await fetch(`${BASE_URL}/products?limit=100`);
//       const data = await res.json();
//       setProducts(data.products || []);
//     } catch (err) {
//       console.error(err);
//       setProducts([]);
//     }
//   };

//   useEffect(() => {
//     fetchProducts();
//   }, []);

//   const handleChange = (field, value) => {
//     setForm(prev => ({ ...prev, [field]: value }));
//   };

//   const handleSubmit = async () => {
//     setLoading(true);
//     try {
//       const res = await fetch(`${BASE_URL}/products`, {
//         method: "POST",
//         headers: authHeaders(),
//         body: JSON.stringify({
//           category: form.category.toLowerCase(),
//           brand: form.brand,
//           model: form.model,
//           price: Number(form.price),
//           stock: Number(form.stock),
//         }),
//       });

//       const data = await res.json();
//       if (!res.ok) { alert(data.detail || "Error"); return; }

//       alert("Created!");
//       setForm({ category: "", brand: "", model: "", price: "", stock: "" });
//       fetchProducts();
//     } catch (err) {
//       console.error(err);
//       alert("Fetch error");
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleDelete = async (id) => {
//     if (!confirm("Delete product?")) return;
//     try {
//       await fetch(`${BASE_URL}/products/${id}`, {
//         method: "DELETE",
//         headers: authHeaders(),
//       });
//       fetchProducts();
//     } catch (err) {
//       console.error(err);
//     }
//   };

//   const handleEdit = async (product) => {
//     const newPrice = prompt("New price:", product.price);
//     if (!newPrice) return;
//     try {
//       await fetch(`${BASE_URL}/products/${product.id}`, {
//         method: "PATCH",
//         headers: authHeaders(),
//         body: JSON.stringify({ price: Number(newPrice) }),
//       });
//       fetchProducts();
//     } catch (err) {
//       console.error(err);
//     }
//   };

//   return (
//     <div>
//       <h1>Admin Panel</h1>

//       <div>
//         <input placeholder="Category" value={form.category} onChange={e => handleChange("category", e.target.value)} />
//         <input placeholder="Brand" value={form.brand} onChange={e => handleChange("brand", e.target.value)} />
//         <input placeholder="Model" value={form.model} onChange={e => handleChange("model", e.target.value)} />
//         <input type="number" placeholder="Price" value={form.price} onChange={e => handleChange("price", e.target.value)} />
//         <input type="number" placeholder="Stock" value={form.stock} onChange={e => handleChange("stock", e.target.value)} />
//         <button onClick={handleSubmit} disabled={loading}>
//           {loading ? "Creating..." : "Create Product"}
//         </button>
//       </div>

//       <h2>Products</h2>
//       <table border="1" cellPadding="10">
//         <thead>
//           <tr>
//             <th>ID</th><th>Category</th><th>Brand</th>
//             <th>Model</th><th>Price</th><th>Stock</th><th>Actions</th>
//           </tr>
//         </thead>
//         <tbody>
//           {Array.isArray(products) && products.length > 0 ? (
//             products.map((p) => (
//               <tr key={p.id}>
//                 <td>{p.id}</td>
//                 <td>{p.category}</td>
//                 <td>{p.brand}</td>
//                 <td>{p.model}</td>
//                 <td>{p.price}</td>
//                 <td>{p.stock}</td>
//                 <td>
//                   <button onClick={() => handleEdit(p)}>Edit</button>
//                   <button onClick={() => handleDelete(p.id)}>Delete</button>
//                 </td>
//               </tr>
//             ))
//           ) : (
//             <tr><td colSpan="7">No products</td></tr>
//           )}
//         </tbody>
//       </table>
//     </div>
//   );
// }