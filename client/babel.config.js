module.exports = function (api) {

  const presets = [
    [
      '@babel/env',
      {
        useBuiltIns: 'usage',
        corejs: '3'
      },
    ],
    '@babel/preset-react',
  ]

  let plugins = [
    '@babel/plugin-transform-modules-commonjs',
    '@babel/plugin-proposal-class-properties',
    'babel-plugin-styled-components',
    'emotion',
  ]
  if (!api.env('production')) {
    plugins.push(['react-remove-properties', {'properties': ['data-test',]}])
  }

  return {
    presets,
    plugins,
  }
}

