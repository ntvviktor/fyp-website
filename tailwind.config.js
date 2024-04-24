/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');

module.exports = {
    content: ["./webapp/templates/*.html",
              "./webapp/templates/accounts/*.html",
              "./webapp/templates/admin/*.html",
              "./webapp/templates/components/*.html",
              "./webapp/templates/errors/*.html",
              "./webapp/templates/**/*.html",
    ],
    plugins: [
        require("daisyui"),
        require('@tailwindcss/forms'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/typography'),
        require('tailwindcss-children')
    ],
}