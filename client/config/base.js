import {basename, relative, resolve} from 'path'
import merge from 'webpack-merge'
import BundleTracker from 'webpack-bundle-tracker'
import glob from 'glob'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import autoprefixer from 'autoprefixer'
const document_root = '..'

import * as partials from './partials'

const DOMAIN = process.env.DOMAIN || 'localhost'
const PORT = process.env.PORT || 8082
const PROTOCOL = process.env.PROTOCOL || 'http'

export const paths = {
  hot: resolve(__dirname, '../hot'),
  dev: resolve(__dirname, '../dist.dev'),
  prod: resolve(__dirname, '../dist.prod'),
}

// Build a bundle for each directory in pages, except common
const context_path = resolve(__dirname, '..')
const files = glob.sync(resolve(__dirname, '../src/pages/*'))
let entries = {}
files.map(f => {
  const b = basename(f)
  if (b != 'common') {
    entries[b] = ['./' + relative(context_path, f+'/index.js')]
  }
})

export default ({env, options}) => {

  console.log(`Generating base build for ${env.stage}`)
  const isDev = /hot|dev/.test(env.stage)

  const strategy = {
    'module.rules': 'append'
  }

  return merge.strategy(strategy)({
      context: context_path,
      entry: entries,
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
                loader: 'file-loader', options: {
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
                  modules: {
                    localIdentName: '[name]__[local]__[hash:base64:5]',
                  },
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
                      flexbox: 'no-2009',
                    }),
                  ],
                },
              },
              'sass-loader',
            ],
          },
        ]
      },
      resolve: {
        alias: {
          '~': resolve(__dirname, '../src'),
          //'Schedule': resolve(__dirname, '../src/Schedule'),
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
    }
  )
}
