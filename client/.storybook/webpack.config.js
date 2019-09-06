const path = require('path')
const merge = require('webpack-merge')

const constants = {
  NODE_MODULES_DIR: '../node_modules'
}

module.exports = async ({config, env}) => {

  const mapToFolder = (dependencies, folder) =>
    dependencies.reduce((acc, dependency) => {
      return {
        [dependency]: require.resolve(path.join(folder, dependency)),
        ...acc
      }
    }, {});

  const resolve = {
    alias: {
      '~':
        path.resolve(__dirname, '../src'),
      'HomePage':
        path.resolve(__dirname, '../src/HomePage'),
      'FeaturedGarden':
        path.resolve(__dirname, '../src/FeaturedGarden'),
      'static/': path.resolve(__dirname, '../../tennisblock/webpack/static'),
      ...mapToFolder([
          'react', 'react-dom', 'react-dom/server'],
        constants.NODE_MODULES_DIR
      ),
    }
  }

  const custom = {
    module: {
      rules: [
        {
          test: /\.scss$/,
          use: [

            {
              loader: require.resolve('style-loader'),
            },
            {
              loader: require.resolve('css-loader'),
              options: {
                importLoaders: 1,
                modules: {
                  localIdentName: '[name]__[local]__[hash:base64:5]',
                },
              }
            },
            require.resolve('sass-loader'),
          ],
          include: path.resolve(__dirname, "../")
        },
        {
          test: /\.css$/,
          use: [

            {
              loader: require.resolve('style-loader'),
              options: {
                singleton: true
              }
            },
            {
              loader: require.resolve('css-loader'),
            },
          ],
          include: path.resolve(__dirname, '../')
        }
      ]
    },
    resolve: resolve,
    devtool: '#cheap-module-source-map',
  }

  return merge.strategy({
    'module.rules': 'prepend',
    'resolve.alias': 'replace',
  })(config, custom)
}
