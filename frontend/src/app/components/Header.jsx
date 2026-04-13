"use client";

import { useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";


export default function Header() {
  const [user, setUser] = useState(null);
  const [dropdown, setDropdown] = useState(false);

  useEffect(() => {
    const readToken = () => {
      const token = localStorage.getItem("token");
      if (token) setUser(jwtDecode(token));
      else setUser(null);
    };

  readToken();
  window.addEventListener("storage", readToken);
  return () => window.removeEventListener("storage", readToken);
}, []);

  return (
    <header className="w-full h-[148px] bg-[#92BA8E]">
      <div className="w-full h-[148px] bg-[#92BA8E] flex items-center justify-between px-[80px]">

        {/* Left: Logo */}
        <div
          className="text-white"
          style={{
            fontFamily: "var(--font-roboto)",
            fontSize: "45px",
            fontWeight: 400,
          }}
        >
          Electronics
        </div>

        {/* Right: Menu */}
        <nav className="flex gap-[48px]">
          <a
            href="#"
            className="text-white"
            style={{
              fontFamily: "var(--font-inter)",
              fontSize: "20px",
              fontWeight: 500,
            }}
          >
            Home
          </a>
          <a
            href="#"
            className="text-white"
            style={{
              fontFamily: "var(--font-inter)",
              fontSize: "20px",
              fontWeight: 500,
            }}
          >
            About Us
          </a>
          <a
            href="#"
            className="text-white"
            style={{
              fontFamily: "var(--font-inter)",
              fontSize: "20px",
              fontWeight: 500,
            }}
          >
            Contacts
          </a>
          {user ? (
            <div className="relative">
              <span
                className="text-white cursor-pointer"
                style={{ fontFamily: "var(--font-inter)", fontSize: "20px", fontWeight: 500 }}
                onClick={() => setDropdown(!dropdown)}
              >
                {user.name}
              </span>
              {dropdown && (
                <div className="absolute right-0 mt-2 bg-white rounded-lg shadow-lg py-2 w-36">
                  <button
                    className="w-full text-left px-4 py-2 text-sm text-black hover:bg-gray-100"
                    onClick={() => {
                      localStorage.removeItem("token");
                      window.dispatchEvent(new Event("storage"));
                      setDropdown(false);
                    }}
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <a href="/login" className="text-white" style={{ fontFamily: "var(--font-inter)", fontSize: "20px", fontWeight: 500 }}>
              Login
            </a>
          )}

          <button
            className="bg-black text-white px-5 py-2 rounded-[8px]"
            style={{
              fontFamily: "var(--font-inter)",
              fontSize: "16px",
              fontWeight: 500,
            }}
          >
            CART
          </button>
        </nav>
      </div>
    </header>
  );
}