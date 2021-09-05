#!/usr/bin/env sh

mkdir -p ../front-end/out-wbss
for f in ../front-end/js-wbss/*; do
	f=`basename $f`
	./compile.py ../front-end/js-wbss/$f >../front-end/out-wbss/$f
done

cd ../front-end
mkdir -p out out-babel
npm install
npx babel out-wbss --out-dir out-babel --presets react-app/prod
npx webpack --config webpack.config.js
ln data/style.css out/ 2>/dev/null
