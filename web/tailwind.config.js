/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: "#FBBF24", // Amber-400 equivalent for Gold
        secondary: "#10B981", // Emerald-500 for Green accents
        danger: "#EF4444", // Red for drops
        "background-light": "#F3F4F6",
        "background-dark": "#111111", // Deep dark background
        "surface-dark": "#1A1A1A", // Slightly lighter for cards
        "surface-light": "#FFFFFF",
        "border-dark": "#333333",
        "border-light": "#E5E7EB",
        "text-muted-dark": "#9CA3AF",
        "text-muted-light": "#6B7280"
      },
      fontFamily: {
        display: ["var(--font-inter)", "sans-serif"],
        arabic: ["var(--font-tajawal)", "sans-serif"]
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem'
      },
    },
  },
  plugins: [],
}
