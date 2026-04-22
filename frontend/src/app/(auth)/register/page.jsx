"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode"

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleRegister() {
    setError("");
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      setError(data.detail || "Register failed");
      return;
    }

    router.push("/login")
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex flex-col gap-4 w-full max-w-sm p-8 bg-white rounded-2xl">
        <h1
          style={{ fontFamily: "var(--font-inter)", fontWeight: 700, fontSize: "24px" }}
        >
          Register
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
          onKeyDown={(e) => e.key === "Enter" && handleRegister()}
          className="border border-gray-300 rounded-lg px-4 py-2 text-sm outline-none"
        />

        <button
          onClick={handleRegister}
          className="bg-black text-white px-5 py-2 rounded-lg text-sm font-medium"
          style={{ fontFamily: "var(--font-inter)" }}
        >
          Register
        </button>

        <p className="text-sm text-center text-gray-500">
          Already have an account?{" "}
          <a href="/login" className="text-black font-medium underline">
            Login
          </a>
        </p>
      </div>
    </div>
  );
}