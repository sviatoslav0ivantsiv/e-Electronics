"use client";
import { useState, useEffect } from "react";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api';

const s = {
  wrap: { padding: "2rem", maxWidth: 1100, margin: "0 auto", fontFamily: "sans-serif" },
  h1: { fontSize: 22, fontWeight: 500, marginBottom: "1.5rem" },
  h2: { fontSize: 18, fontWeight: 500, margin: "1.5rem 0 1rem" },
  card: { background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 12, padding: "1.25rem" },
  formGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 12, marginBottom: "1rem" },
  input: { width: "100%", height: 36, padding: "0 12px", border: "0.5px solid #ccc", borderRadius: 8, fontSize: 14, outline: "none" },
  select: { width: "100%", height: 36, padding: "0 12px", border: "0.5px solid #ccc", borderRadius: 8, fontSize: 14, background: "#fff" },
  textarea: { width: "100%", padding: "8px 12px", border: "0.5px solid #ccc", borderRadius: 8, fontSize: 14, outline: "none", resize: "vertical", minHeight: 72 },
  btn: { height: 36, padding: "0 16px", border: "0.5px solid #ccc", borderRadius: 8, fontSize: 14, background: "transparent", cursor: "pointer" },
  btnPrimary: { background: "#e8f1fb", color: "#185fa5", border: "0.5px solid #b5d4f4", borderRadius: 8, height: 36, padding: "0 16px", fontSize: 14, cursor: "pointer" },
  btnDanger: { background: "#fcebeb", color: "#a32d2d", border: "0.5px solid #f7c1c1", borderRadius: 8, height: 36, padding: "0 16px", fontSize: 14, cursor: "pointer" },
  btnSuccess: { background: "#eaf3de", color: "#3b6d11", border: "0.5px solid #c0dd97", borderRadius: 8, height: 36, padding: "0 16px", fontSize: 14, cursor: "pointer" },
  table: { width: "100%", borderCollapse: "collapse", fontSize: 14 },
  th: { textAlign: "left", padding: "10px 12px", fontWeight: 500, fontSize: 13, color: "#888", borderBottom: "0.5px solid #e0e0e0" },
  td: { padding: "10px 12px", borderBottom: "0.5px solid #f0f0f0" },
  badge: { display: "inline-block", padding: "2px 8px", borderRadius: 6, fontSize: 12, background: "#e8f1fb", color: "#185fa5" },
  badgeAdmin: { display: "inline-block", padding: "2px 8px", borderRadius: 6, fontSize: 12, background: "#eaf3de", color: "#3b6d11" },
  badgeUser: { display: "inline-block", padding: "2px 8px", borderRadius: 6, fontSize: 12, background: "#f1efe8", color: "#5f5e5a" },
  overlay: { position: "fixed", inset: 0, background: "rgba(0,0,0,0.4)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100, overflowY: "auto" },
  modal: { background: "#fff", borderRadius: 12, padding: "1.5rem", width: 480, border: "0.5px solid #e0e0e0", margin: "2rem auto" },
  tab: (active) => ({ height: 36, padding: "0 20px", border: "none", borderBottom: active ? "2px solid #185fa5" : "2px solid transparent", background: "transparent", fontSize: 15, fontWeight: active ? 500 : 400, color: active ? "#185fa5" : "#888", cursor: "pointer" }),
  label: { fontSize: 12, color: "#888", marginBottom: 4, display: "block" },
};

const EMPTY_FORM = {
  category: "laptop", brand: "", model: "", price: "", stock: "",
  description: "", display_size: "", battery_capacity: "", camera_mp: "",
  cpu: "", gpu: "", screen_size: "", weight: "",
  screen_type: "", battery_life: "", water_resistance: "",
  ram: "", storage: ""
};

const CATEGORY_FIELDS = {
  smartphone: ["display_size", "battery_capacity", "camera_mp", "ram", "storage"],
  laptop: ["cpu", "gpu", "screen_size", "weight", "ram", "storage"],
  smartwatch: ["screen_type", "battery_life", "water_resistance"],
};

const FIELD_META = {
  display_size:      { label: "Display size (in)", type: "number" },
  battery_capacity:  { label: "Battery capacity (mAh)", type: "number" },
  camera_mp:         { label: "Camera (MP)", type: "number" },
  cpu:               { label: "CPU", type: "text" },
  gpu:               { label: "GPU", type: "text" },
  screen_size:       { label: "Screen size (in)", type: "number" },
  weight:            { label: "Weight (kg)", type: "number" },
  screen_type:       { label: "Screen type", type: "text" },
  battery_life:      { label: "Battery life (hrs)", type: "number" },
  water_resistance:  { label: "Water resistance", type: "text" },
  ram:               { label: "RAM (GB)", type: "number" },
  storage:           { label: "Storage (GB)", type: "number" },
};



function ProductForm({ form, setForm, onSubmit, loading, title, onCancel }) {
  const extraFields = CATEGORY_FIELDS[form.category] || [];

  const handleChange = (field, value) =>
    setForm(prev => ({ ...prev, [field]: value }));

  const clean = (f) => {
    const val = f[field];
    return val === "" || val === null ? null : isNaN(val) ? val : Number(val);
  };

  return (
    <div>
      <h2 style={{ ...s.h2, marginTop: 0 }}>{title}</h2>

      <div style={s.formGrid}>
        <div>
          <label style={s.label}>Category</label>
          <select style={s.select} value={form.category}
            onChange={e => setForm(prev => ({ ...prev, category: e.target.value }))}>
            <option value="laptop">Laptop</option>
            <option value="smartphone">Smartphone</option>
            <option value="smartwatch">Smartwatch</option>
          </select>
        </div>
        {["brand", "model"].map(f => (
          <div key={f}>
            <label style={s.label}>{f.charAt(0).toUpperCase() + f.slice(1)}</label>
            <input style={s.input} placeholder={f} value={form[f]}
              onChange={e => handleChange(f, e.target.value)} />
          </div>
        ))}
        <div>
          <label style={s.label}>Price ($)</label>
          <input style={s.input} type="number" placeholder="Price" value={form.price}
            onChange={e => handleChange("price", e.target.value)} />
        </div>
        <div>
          <label style={s.label}>Stock</label>
          <input style={s.input} type="number" placeholder="Stock" value={form.stock}
            onChange={e => handleChange("stock", e.target.value)} />
        </div>
      </div>

      <div style={{ marginBottom: 12 }}>
        <label style={s.label}>Description</label>
        <textarea style={s.textarea} placeholder="Description..." value={form.description || ""}
          onChange={e => handleChange("description", e.target.value)} />
      </div>

      {extraFields.length > 0 && (
        <>
          <p style={{ fontSize: 13, color: "#888", marginBottom: 10 }}>
            {form.category} specs
          </p>
          <div style={s.formGrid}>
            {extraFields.map(f => (
              <div key={f}>
                <label style={s.label}>{FIELD_META[f].label}</label>
                <input style={s.input} type={FIELD_META[f].type} placeholder={FIELD_META[f].label}
                  value={form[f]} onChange={e => handleChange(f, e.target.value)} />
              </div>
            ))}
          </div>
        </>
      )}

      <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
        <button style={s.btnPrimary} onClick={onSubmit} disabled={loading}>
          {loading ? "Saving..." : "Save"}
        </button>
        {onCancel && <button style={s.btn} onClick={onCancel}>Cancel</button>}
      </div>
    </div>
  );
}

export default function AdminPage() {
  const [tab, setTab] = useState("products");
  const [form, setForm] = useState(EMPTY_FORM);
  const [products, setProducts] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editProduct, setEditProduct] = useState(null);
  const [deleteId, setDeleteId] = useState(null);

  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      window.location.href = "/products";
      return;
    }

    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      setUser(payload);

      if (!payload.is_admin) {
        window.location.href = "/products";
      }
    } catch {
      window.location.href = "/products";
    }
  }, []);

  const getToken = () => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
  };
  const authHeaders = () => ({
    "Content-Type": "application/json",
    "Authorization": `Bearer ${getToken()}`
  });

  console.log("headers", authHeaders());  

  const fetchProducts = async () => {
    try {
      const res = await fetch(`${BASE_URL}/products?limit=100`);
      const data = await res.json();
      setProducts(data.products || []);
    } catch (err) { setProducts([]); }
  };

  const fetchUsers = async () => {
    try {
      const res = await fetch(`${BASE_URL}/admin/users`, { headers: authHeaders() });
      const data = await res.json();
      setUsers(Array.isArray(data) ? data : []);
    } catch (err) { setUsers([]); }
  };

  useEffect(() => {
    if (!user?.is_admin) return;

    fetchProducts();
    fetchUsers();
}, [user]);

  if (!user) return null;

  const buildPayload = (f) => {
    const extraFields = CATEGORY_FIELDS[f.category] || [];
    const allFields = ["brand", "model", "price", "stock", "description", ...extraFields];
    const payload = { category: f.category };
    allFields.forEach(field => {
      const val = f[field];
      if (val === "" || val === null || val === undefined) {
        payload[field] = null;
      } else {
        payload[field] = isNaN(val) ? val : Number(val);
      }
    });
    return payload;
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/products`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(buildPayload(form)),
      });
      const data = await res.json();
      if (!res.ok) { alert(data.detail || "Error"); return; }
      setForm(EMPTY_FORM);
      fetchProducts();
    } catch (err) { alert("Fetch error"); }
    finally { setLoading(false); }
  };

  const handleEditSave = async () => {
    try {
      await fetch(`${BASE_URL}/products/${editProduct.id}`, {
        method: "PATCH",
        headers: authHeaders(),
        body: JSON.stringify(buildPayload(editProduct)),
      });
      setEditProduct(null);
      fetchProducts();
    } catch (err) { console.error(err); }
  };

  const handleDelete = async (id) => {
    if (deleteId !== id) {
      setDeleteId(id);
      return;
    }
    try {
      const res = await fetch(`${BASE_URL}/products/${id}`, {
        method: "DELETE",
        headers: authHeaders(),
      });
      console.log("delete status", res.status);
      setDeleteId(null);
      fetchProducts();
    } catch (err) { console.error(err); }
  };

  const handleToggleAdmin = async (userId) => {
    try {
      await fetch(`${BASE_URL}/admin/users/${userId}/toggle-admin`, {
        method: "PATCH", headers: authHeaders(),
      });
      fetchUsers();
    } catch (err) { console.error(err); }
  };

  return (
    <div style={s.wrap}>
      <h1 style={s.h1}>Admin panel</h1>

      <div style={{ borderBottom: "0.5px solid #e0e0e0", marginBottom: "1.5rem", display: "flex" }}>
        <button style={s.tab(tab === "products")} onClick={() => setTab("products")}>Products</button>
        <button style={s.tab(tab === "users")} onClick={() => setTab("users")}>Users</button>
      </div>

      {tab === "products" && (
        <>
          <div style={s.card}>
            <ProductForm form={form} setForm={setForm}
              onSubmit={handleSubmit} loading={loading} title="Add product" />
          </div>

          <h2 style={s.h2}>All products</h2>
          <div style={{ ...s.card, padding: 0, overflow: "hidden" }}>
            <table style={s.table}>
              <thead>
                <tr>
                  {["ID", "Category", "Brand", "Model", "Price", "Stock", "Actions"].map(h => (
                    <th key={h} style={s.th}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {products.length > 0 ? products.map(p => (
                  <tr key={p.id}>
                    <td style={s.td}>{p.id}</td>
                    <td style={s.td}><span style={s.badge}>{p.category}</span></td>
                    <td style={s.td}>{p.brand}</td>
                    <td style={s.td}>{p.model}</td>
                    <td style={s.td}>${p.price}</td>
                    <td style={s.td}>{p.stock}</td>
                    <td style={s.td}>
                      <div style={{ display: "flex", gap: 8 }}>
                        <button style={s.btn} onClick={() => setEditProduct({ ...EMPTY_FORM,
                          ...Object.fromEntries(Object.entries(p).filter(([_, v]) => v !== null)) })}>Edit</button>
                        <button 
                          style={deleteId === p.id ? s.btnDanger : s.btn} 
                          onClick={() => handleDelete(p.id)}
                        >
                          {deleteId === p.id ? " Del? " : "Delete"}
                        </button>
                      </div>
                    </td>
                  </tr>
                )) : (
                  <tr><td style={s.td} colSpan={7}>No products</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}

      {tab === "users" && (
        <>
          <h2 style={s.h2}>All users</h2>
          <div style={{ ...s.card, padding: 0, overflow: "hidden" }}>
            <table style={s.table}>
              <thead>
                <tr>
                  {["ID", "Name", "Role", "Created at", "Actions"].map(h => (
                    <th key={h} style={s.th}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {users.length > 0 ? users.map(u => (
                  <tr key={u.id}>
                    <td style={s.td}>{u.id}</td>
                    <td style={s.td}>{u.name}</td>
                    <td style={s.td}>
                      <span style={u.is_admin ? s.badgeAdmin : s.badgeUser}>
                        {u.is_admin ? "admin" : "user"}
                      </span>
                    </td>
                    <td style={s.td}>{new Date(u.created_at).toLocaleDateString()}</td>
                    <td style={s.td}>
                      <button
                        style={u.is_admin ? s.btnDanger : s.btnSuccess}
                        onClick={() => handleToggleAdmin(u.id)}>
                        {u.is_admin ? "Revoke admin" : "Make admin"}
                      </button>
                    </td>
                  </tr>
                )) : (
                  <tr><td style={s.td} colSpan={5}>No users</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}

      {editProduct && (
        <div style={s.overlay}>
          <div style={s.modal}>
            <ProductForm
              form={editProduct}
              setForm={setEditProduct}
              onSubmit={handleEditSave}
              loading={false}
              title={`Edit — ${editProduct.model}`}
              onCancel={() => setEditProduct(null)}
            />
          </div>
        </div>
      )}
    </div>
  );
}