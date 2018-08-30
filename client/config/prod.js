import merge from 'webpack-merge';

import baseConfigFunc from './base';
import {resolve} from "path";

export default ({env, options}) => {

    const strategy = {
        'output.path': 'replace',
        'output.filename': 'replace',
        'module.rules': 'append',
        'plugins': 'append',
    };

    const baseConfig = baseConfigFunc({env, options})

    var output = {
        filename: 'js/[name]_[hash].js',
    }

    return merge.strategy(strategy)(
        baseConfig,
        {
            output: output,
        }
    )
}
