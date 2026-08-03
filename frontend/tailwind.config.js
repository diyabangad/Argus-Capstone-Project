/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      colors: {
        argus: {
          bg: "#f8fafc",
          panel: "#ffffff",
          "panel-soft": "#f1f5f9",
          line: "#e2e8f0",
          text: "#111827",
          muted: "#64748b",
          accent: "#2563eb"
        }
      },
      boxShadow: {
        soft: "0 18px 45px rgba(15, 23, 42, 0.08)"
      }
    }
  },
  plugins: []
};
