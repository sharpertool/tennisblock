module.exports = {
  modulePathIgnorePatterns: [
    'cypress/*',
    'node_modules'
  ],
  moduleNameMapper: {
    ['~/(.*)']: '<rootDir>/src/$1',
    ['\\.local\\.(css|scss)$']: 'identity-obj-proxy'
  },
  roots: [
    '<rootDir>'
  ],
  testMatch: [
    './__tests__/**/*.(spec|test).js',
  ],
  collectCoverage: false,
  transformIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/stories/',
    '<rootDir>/.storybook/',
    '<rootDir>/dist.prod/',
    '<rootDir>/dist.dev/',
    '<rootDir>/hot/',
    '<rootDir>/scripts/',
    '<rootDir>/dist.analyze/',
    '<rootDir>/cypress/',
    'jasmine2Initializer',
    '\\.local\\.scss$'
  ],
  transform: {
    ['^.+\\.jsx?$']: 'babel-jest',
    ['\\.(scss|css)$']: '<rootDir>/styleMocks.js'
  },
  unmockedModulePathPatterns: [
    'react',
    'enzyme',
    'jest-enzyme'
  ],
  testURL: 'http://localhost/',
  setupFilesAfterEnv: [
    '<rootDir>/enzyme_config.js'
  ]
}
