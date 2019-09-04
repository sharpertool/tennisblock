import {resolve, basename} from 'path'
import merge from 'webpack-merge'
import BundleTracker from 'webpack-bundle-tracker'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import glob from 'glob'
import * as partials from './partials'

const document_root = '..'
const dj_root = resolve(__dirname, '../../tennisblock')

const DOMAIN = process.env.DOMAIN || 'tennisblock.local'
const PORT = process.env.PORT || 8081
const PROTOCOL = process.env.PROTOCOL || 'https'

export const paths = {
  hot: resolve(__dirname, '../hot'),
  dev: resolve(dj_root, './static'),
  prod: resolve(dj_root, './static'),
  circleci: resolve(__dirname, '../dist.prod')
}

const files = glob.sync(resolve(__dirname, '../../tennisblock/webapp/static/scss/[^_]*.scss'))
console.log(`Files: ${files}`)
let entries = {}
files.map(f => {
  const b = basename(f, '.scss')
  entries[b] = f
})
console.log(entries)

export default ({env, options}) => {
  
  if (options.verbose) {
    console.log(`Generating base build for ${env.stage}`)
    
  }
  const isDev = /hot|dev/.test(env.stage)
  
  const strategy = {
    'module.rules': 'append'
  }
  
  console.log(`Dirname ${__dirname}`)
  
  return merge.strategy(strategy)({
      entry: entries,
      mode: options.mode || 'development',
      output: {
        path: paths[env.stage],
        publicPath: '/static/',
        filename: 'js_webpack/[name].[hash].js',
      },
      resolve: {
        alias: {
          'Static': resolve(dj_root, 'static'),
        }
      },
      plugins: [
        new BundleTracker({
          path: paths[env.stage],
          filename: 'webpack-assets-stats.json',
          logTime: true,
          indent: 4,
        }),
        new MiniCssExtractPlugin({
          filename: isDev ? 'css_webpack/[name].css' : 'css/[name]_[hash].css',
          chunkFilename: '[id].css',
        }),
      ]
    },
    partials.loadFonts({isDev: isDev}),
    partials.loadSCSS({isDev: isDev}),
  )
}
