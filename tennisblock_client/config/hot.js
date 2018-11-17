import map from 'lodash/map'
import baseConfig, {paths} from './base'
import merge from 'webpack-merge'
import fs from 'fs'
import {join, resolve} from 'path'
import {devServer} from './partials'
import BundleTracker from 'webpack-bundle-tracker'

const DOMAIN = process.env.DOMAIN || 'tennisblock.local'
const PORT = process.env.PORT || 8081
const PROTOCOL = process.env.PROTOCOL || 'http'

const rules = [
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
  {
    test: /\.(sa|sc|c)ss$/,
    exclude: /node_modules/,
    use: [
      {
        loader: 'style-loader', options: {
          sourceMap: true
        }
      },
      {
        loader: 'css-loader', options: {
          sourceMap: true,
          modules: true,
          importLoaders: 1,
          localIdentName: '[name]__[local]__[hash:base64:5]',
        }
      },
      {
        loader: 'sass-loader', options: {
          sourceMap: true
        }
      }
    ]
  }
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
      '.gardenbuzz.local',
      'dev.gardenbuzz.local',
      `${DOMAIN}`
    ]
  }))
}
