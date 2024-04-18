/* Copyright (c) 2020 Paul Barker <paul@pbarker.dev>
 * SPDX-License-Identifier: CC0-1.0
 */

module.exports = {
  content: ["./theme/templates/*.html"],
  theme: {
    extend: {}
  },
  variants: {},
  plugins: [
    require('@tailwindcss/typography'),
  ]
};
