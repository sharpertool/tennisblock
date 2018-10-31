import {resolve} from 'path';
import merge from 'webpack-merge'

import baseConfigFunc from './base'

module.exports = ({env, options}) => {
    const strategy = {
        'output.path': 'replace',
        'output.filename': 'replace',
        'module.rules': 'append',
    };

    console.log(`Set  path to include ${process.env.FRONTEND_PATH}`)

    console.log(`Merging base build and dev for ${env.stage}`)
    const baseConfig = baseConfigFunc({env, options})
    console.log(`base: ${JSON.stringify(baseConfig)}`)

    var output = {}

    return merge.strategy(strategy)(
        baseConfig,
        {
            output: output,
        }
    )
}
