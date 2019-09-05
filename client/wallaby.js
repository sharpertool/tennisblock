module.exports = function(wallaby) {
  console.log(wallaby)
  return {
    files: [
      'src/**/*.+(scss|css)',
      'src/**/*.js',
      '__tests__/**/*.json',
      'jest.config.js',
      'styleMocks.js',
      'enzyme_config.js',
    ],
    
    tests: [
      '__tests__/**/*.+(spec|test).js',
    ],
    env: {
      type: 'node',
      runner: 'node'
    },
    compilers: {
      '**/*.js': wallaby.compilers.babel()
    },
    testFramework: 'jest',
    setup: function(wallaby) {
      var jestConfig = require('./jest.config')
      jestConfig.globals = {'__DEV__': true}
      wallaby.testFramework.configure(jestConfig)
    }
    //debug: true
  }
}
