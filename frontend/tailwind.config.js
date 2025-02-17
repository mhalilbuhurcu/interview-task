/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/pages/**/*.{js,jsx,ts,tsx}", // Adjust this path based on your project structure
      "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
      "./src/styles/globals.css", // Ensure this path is included
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  } 