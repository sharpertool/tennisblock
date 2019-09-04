module.exports = function(wallaby) {
  return {
    files: [
      'src/**/*.js',
      './*.js'
    ],
    
    tests: [
      '__test__/**/*.js'
    ],
    env: {
      type: 'node',
      runner: 'node'
    },
    compilers: {
      '**/*.js?(x)': wallaby.compilers.babel()
    },
    testFramework: 'jest',
    setup: function(wallaby) {
      var jestConfig = require('./package.json').jest
      jestConfig.globals = {'__DEV__': true}
      wallaby.testFramework.configure(jestConfig)
    },
    debug: true
  }
}
