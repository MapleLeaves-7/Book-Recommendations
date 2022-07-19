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
      boxShadow: {
        button: '2px 2px 2px rgba(0, 0, 0, 0.1)',
        'main-card': '3px 4px 5px rgba(0, 0, 0, 0.20)',
        'sub-card': '0px 4px 15px rgba(0, 0, 0, 0.20)',
        search: '0px 3px 5px 3px rgba(0, 0, 0, 0.20)',
      },
    },
  },
  plugins: [],
};
