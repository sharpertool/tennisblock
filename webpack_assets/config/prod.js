import merge from 'webpack-merge'
import UglifyJsPlugin from "uglifyjs-webpack-plugin"
import OptimizeCSSAssetsPlugin from "optimize-css-assets-webpack-plugin"
import baseConfigFunc from './base'
import {resolve} from "path"

export default ({env, options={mode:'production'}}) => {
  
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
    filename: 'js/[name]_[hash].js',
    publicPath: `/static/`,
    chunkFilename: '[name].[chunkhash].bundle.js',
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
