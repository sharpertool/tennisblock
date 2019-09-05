import merge from 'webpack-merge'
const CompressionPlugin = require('compression-webpack-plugin')
const SentryCliPlugin = require('@sentry/webpack-plugin');

import baseConfigFunc, {paths} from './base'
import {resolve} from 'path'

const rules = []

export default ({env, options}) => {
  
  const strategy = {
    'output.path': 'replace',
    'output.filename': 'replace',
    'output.publicPath': 'replace',
    entry: 'prepend',
    'module.rules': 'append'
  }
  
  const baseConfig = baseConfigFunc({env, options})
  
  var output = {
    filename: 'js/[name]_[hash].js',
    publicPath: '/static/',
    chunkFilename: '[name].k[chunkhash].bundle.js',
  }
  
  return merge.strategy(strategy)(
    baseConfig,
    {
      devtool: 'source-map',
      output: output,
    },
    {
      optimization: {
        splitChunks: {
          cacheGroups: {
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              chunks: 'all',
              name: 'vendor',
              enforce: true
            },
          }
        }
      },
      plugins: [
        new CompressionPlugin(),
      ]
    },
  )
}
