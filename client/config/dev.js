import baseConfig, {paths} from './base'
import merge from 'webpack-merge'

const rules = []

export default ({env, options}) => {
  
  const strategy = {
    entry: 'prepend',
    output: 'append',
    'output.publicPath': 'replace',
    'module.rules': 'append'
  }
  
  const mainConfig = baseConfig({env, options})
  
  
  return merge.strategy(strategy)(
    mainConfig,
    {
      optimization: {
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
    {
      devtool: 'source-map',
      mode: 'development',
      module: {
        rules
      },
      output: {
        publicPath: '/static/'
      }
    },
  )
}
