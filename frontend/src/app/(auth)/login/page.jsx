"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode"

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function LoginPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin() {
    setError("");
    const res = await fetch(`${BASE_URL.replace('/api', '')}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      setError(data.detail || "Login failed");
      return;
    }

    localStorage.setItem("token", data.token);
    window.dispatchEvent(new Event("storage"));
    const decoded = jwtDecode(data.token);
    router.push(decoded.is_admin ? "/admin" : "/products");
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="flex flex-col gap-4 w-full max-w-sm p-8 bg-white rounded-2xl">
        <h1
          style={{ fontFamily: "var(--font-inter)", fontWeight: 700, fontSize: "24px" }}
        >
          Login
        </h1>

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <input
          type="text"
          placeholder="Username"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border border-gray-300 rounded-lg px-4 py-2 text-sm outline-none"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleLogin()}
          className="border border-gray-300 rounded-lg px-4 py-2 text-sm outline-none"
        />

        <button
          onClick={handleLogin}
          className="bg-black text-white px-5 py-2 rounded-lg text-sm font-medium"
          style={{ fontFamily: "var(--font-inter)" }}
        >
          Login
        </button>

        <p className="text-sm text-center text-gray-500">
          Don't have an account?{" "}
          <a href="/register" className="text-black font-medium underline">
            Register
          </a>
        </p>
      </div>
    </div>
  );
}