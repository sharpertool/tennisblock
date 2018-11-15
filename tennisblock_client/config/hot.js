import map from 'lodash/map'
import baseConfig, {paths} from './base'
import merge from 'webpack-merge'
import fs from 'fs'
import {join, resolve} from 'path'
import {devServer} from './partials'
import BundleTracker from 'webpack-bundle-tracker'
import autoprefixer from 'autoprefixer'
const DOMAIN = process.env.DOMAIN || 'tennisblock.local'
const PORT = process.env.PORT || 8081
const PROTOCOL = 'http'

const rules = [
  {
    test: /\.js$/,
    enforce: 'pre',
    exclude: /node_modules/,
    loader: 'eslint-loader',
    options: {
      fix: true
    },
  },
  {
    test: /\.js$/,
    exclude: /node_modules/,
    loader: 'babel-loader'
  },
  {
    test: /\.(jpe|jpg|woff|woff2|eot|ttf|svg)(\?.*$|$)/,
    use: [
      {
        loader: 'url-loader', options: {
          limit: 8192
        }
      }
    ]
  },
  // "postcss" loader applies autoprefixer to our CSS.
  // "css" loader resolves paths in CSS and adds assets as dependencies.
  // "style" loader turns CSS into JS modules that inject <style> tags.
  // In production, we use a plugin to extract that CSS to a file, but
  // in development "style" loader enables hot editing of CSS.
  {
    test: /\.(scss|css)$/,
    exclude: /\.local\.(scss|css)/,
    use: [
      require.resolve('style-loader'),
      {
        loader: require.resolve('css-loader'),
        options: {
        },
      },
      {
        loader: require.resolve('postcss-loader'),
        options: {
          // Necessary for external CSS imports to work
          // https://github.com/facebookincubator/create-react-app/issues/2677
          ident: 'postcss',
          plugins: () => [
            require('postcss-flexbugs-fixes'),
            autoprefixer({
              browsers: [
                '>1%',
                'last 4 versions',
                'Firefox ESR',
                'not ie < 9', // React doesn't support IE8 anyway
              ],
              flexbox: 'no-2009',
            }),
          ],
        },
      },
      'sass-loader',
    ],
  },
  // This loader supports modules, with the .local.* suffix
  // "css" loader resolves paths in CSS and adds assets as dependencies.
  // "style" loader turns CSS into JS modules that inject <style> tags.
  // In production, we use a plugin to extract that CSS to a file, but
  // in development "style" loader enables hot editing of CSS.
  {
    test: /\.local\.(scss|css)$/,
    use: [
      require.resolve('style-loader'),
      {
        loader: require.resolve('css-loader'),
        options: {
          importLoaders: 1,
          modules: true,
          localIdentName: '[name]__[local]__[hash:base64:5]',
        },
      },
      {
        loader: require.resolve('postcss-loader'),
        options: {
          // Necessary for external CSS imports to work
          // https://github.com/facebookincubator/create-react-app/issues/2677
          ident: 'postcss',
          plugins: () => [
            require('postcss-flexbugs-fixes'),
            autoprefixer({
              browsers: [
                '>1%',
                'last 4 versions',
                'Firefox ESR',
                'not ie < 9', // React doesn't support IE8 anyway
              ],
              flexbox: 'no-2009',
            }),
          ],
        },
      },
      'sass-loader',
    ],
  },
]

export default ({env, options}) => {

  const strategy = {
    entry: 'prepend',
    output: 'append',
    'output.publicPath': 'replace',
    'module.rules': 'replace'
  }

  const mainConfig = baseConfig({env, options})
  const baseEntry = mainConfig.entry
  const entry = {}

  map(baseEntry, (v, k) => {
    entry[k] = [
      'react-hot-loader/patch',
      //Dev server bundle
      `webpack-dev-server/client?${PROTOCOL}://${DOMAIN}:${PORT}`,
      //Only reload successful updates
      'webpack/hot/only-dev-server'
    ]
  })

  return merge.strategy(strategy)(mainConfig, {
    devtool: 'source-map',
    entry,
    module: {
      rules
    },
    output: {
      publicPath: `${PROTOCOL}://${DOMAIN}:${PORT}/hot/`
    }
  }, devServer({
    hot: true,
    https: env.https ? {
      key: fs.readFileSync('../ssl/private.key'),
      cert: fs.readFileSync('../ssl/private.crt'),
      ca: fs.readFileSync('../ssl/private.pem')
    } : false,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
    },
    port: PORT,
    protocol: `${PROTOCOL}`,
    base: paths.hot,
    allowedHosts: [
      '.tennisblock.local',
      `${DOMAIN}`,
    ]

  }))
}
