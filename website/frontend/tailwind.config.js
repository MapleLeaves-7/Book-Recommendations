/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        arvo: ['Arvo', 'sans-serif'],
        titillium: ['Titillium Web', 'sans-serif'],
      },
      colors: {
        banner: '#CB997E',
        bg: '#FFFEF5',
        'off-white': '#FEFEFE',
        button: '#A5A58D',
      },
    },
  },
  plugins: [],
};
