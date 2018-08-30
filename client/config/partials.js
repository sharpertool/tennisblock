import cors from 'cors'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'

export const devServer = ({hot, host, port, base} = {}) => ({
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
})

export const loadFonts = ({include, exclude} = {}) => ({
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
                test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
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

export const loadSCSS = ({include, exclude, isDev} = {isDev:true}) => ({
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                exclude: /node_modules/,
                use: [
                    isDev ? 'style-loader' : MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader',
                    'sass-loader'
                ]
            }
        ],
    }
})
