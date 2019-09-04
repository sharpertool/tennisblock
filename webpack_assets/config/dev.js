import {resolve} from 'path';
import merge from 'webpack-merge'

import baseConfigFunc from './base'

module.exports = ({env, options}) => {
  const strategy = {
    'output.path': 'replace',
    'output.filename': 'replace',
    'module.rules': 'append',
  };

  if (options.verbose) {
    console.log(`Set  path to include ${process.env.FRONTEND_PATH}`)
  }

  if (options.verbose) {
    console.log(`Merging base build and dev for ${env.stage}`)
  }
  const baseConfig = baseConfigFunc({env, options})

  if (options.verbose) {
    console.log(`base: ${JSON.stringify(baseConfig)}`)
  }

  return merge.strategy(strategy)(
    baseConfig,
  )
}
