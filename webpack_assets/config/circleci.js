import merge from 'webpack-merge'

import baseConfigFunc from './base'
import {resolve} from "path"
import UglifyJsPlugin from "uglifyjs-webpack-plugin"
import OptimizeCSSAssetsPlugin from "optimize-css-assets-webpack-plugin"

export default ({env, options}) => {
  
  //console.log('Prod Options are ', options);
  console.log('Prod environment is ', env)
  
  const strategy = {
    'output.path': 'replace',
    'output.filename': 'replace',
    'output.publicPath': 'replace',
    'module.rules': 'append',
    'plugins': 'append',
  }
  
  const baseConfig = baseConfigFunc({env, options})
  
  var output = {
    filename: 'js/[name].[hash].js',
  }
  
  return merge.strategy(strategy)(
    baseConfig,
    {
      output: output,
    },
    {
      optimization: {
        minimizer: [
          new UglifyJsPlugin({
            cache: true,
            parallel: true,
            sourceMap: true // set to true if you want JS source maps
          }),
          new OptimizeCSSAssetsPlugin({})
        ],
        splitChunks: {
          cacheGroups: {
            vendor: {
              test: /node_modules/,
              chunks: 'initial',
              name: 'vendor',
              enforce: true
            },
          }
        }
      }
    },
  )
}
