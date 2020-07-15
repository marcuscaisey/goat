const path = require("path");

module.exports = {
  mode: "production",
  entry: {
    "js/base": "./js/base.js",
  },
  output: {
    path: path.resolve(__dirname, "static"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        include: path.resolve(__dirname, "./js"),
        loader: "babel-loader",
      },
    ],
  },
};
