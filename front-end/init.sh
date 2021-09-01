#!/usr/bin/env sh

mkdir -p out out-babel
npm install
npx babel js --out-dir out-babel --presets react-app/prod
npx webpack --config webpack.config.js
ln data/style.css out/
