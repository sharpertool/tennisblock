import {resolve} from 'path'
import merge from 'webpack-merge'
import BundleTracker from 'webpack-bundle-tracker'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'

const document_root = '..'

import * as partials from './partials'

const DOMAIN = process.env.DOMAIN || 'localhost'
const PORT = process.env.PORT || 8080
const PROTOCOL = process.env.PROTOCOL || 'https'

export const paths = {
  hot: resolve(__dirname, '../hot'),
  dev: resolve(__dirname, '../dist.dev'),
  prod: resolve(__dirname, '../dist.prod'),
}

export default ({env, options}) => {

  console.log(`Generating base build for ${env.stage}`)
  const isDev = /hot|dev/.test(env.stage)

  const strategy = {
    'module.rules': 'append'
  }

  return merge.strategy(strategy)({
      entry: {
        Availability: [resolve(__dirname, `${document_root}/src/Availability/index.js`)],
        Schedule: [resolve(__dirname, `${document_root}/src/Schedule/index.js`)],
        Home: [resolve(__dirname, `${document_root}/src/containers/Home/index.js`)]
      },
      mode: options.mode,
      output: {
        path: paths[env.stage],
        publicPath: '/static/',
        filename: 'js/[name].js',
        libraryTarget: 'var',
        library: '[name]',
        libraryExport: 'default',
      },
      module: {
        rules: [
          {
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
          },
        ]
      },
      resolve: {
        alias: {
          '~': resolve(__dirname, '../src'),
          'Schedule': resolve(__dirname, '../src/Schedule'),
        }
      },
      plugins: [
        new BundleTracker({
          path: paths[env.stage],
          filename: 'webpack-stats.json',
          logTime: true,
          indent: 4,
        }),
        new MiniCssExtractPlugin({
          filename: isDev ? 'css/[name].css' : 'css/[name]_[hash].css',
          chunkFilename: '[id].css',
        }),
      ]
    },
    partials.loadSCSS({isDev: isDev}),
    partials.loadFonts(),
  )
}
