const path = require('path');

module.exports = {
  entry: './out-babel/configuration.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'out/'),
  },
  mode: 'development',
};
