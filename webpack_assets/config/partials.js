import {resolve} from 'path'
import cors from 'cors'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import autoprefixer from 'autoprefixer'

export const devServer = ({
                            hot, host, port,
                            base,
                            https = false,
                            cert = null,
                            allowedHosts = null
                          } = {}) => {
  const config = {
    devServer: {
      hot,
      contentBase: base,
      historyApiFallback: true,
      overlay: {
        errors: true,
        warnings: true,
      },
      port,
      before(app) {
        app.use(cors())
      }
    }
  }
  
  if (allowedHosts) {
    config.devServer.allowedHosts = allowedHosts
  }
  
  if (https) {
    config.devServer.https = https
    console.log('Configured as https')
  }
  
  return config
}

export const loadFonts = ({include, exclude, isDev} = {}) => ({
  module: {
    rules: [
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 8192,
              mimetype: 'application/font-woff',
              name: 'assets/[name].[ext]',
              publicPath: '/static/'
            }
          }
        ]
      },
      {
        test: /\.(ttf|eot|otf|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: 'assets/[name].[ext]',
              publicPath: '/static/'
            }
          }
        ]
      }
    ]
  }
  
})

export const loadSCSS = ({include, exclude, isDev} = {isDev: true}) => ({
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        exclude: /node_modules/,
        use: [
          //isDev ? require.resolve('style-loader') : MiniCssExtractPlugin.loader,
          // {
          //   loader: 'file-loader',
          //   options: {
          //     name: 'css_webpack/[name].[hash].css',
          //   }
          // },
          // {
          //   loader: 'extract-loader',
          // },
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: require.resolve('css-loader'),
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
          'resolve-url-loader',
          {
            loader: 'sass-loader',
            options: {
              sassOptions: {
                includePaths: [
                  'node_modules',
                ],
              },
            },
          },
        ]
      }
    ],
  }
})
