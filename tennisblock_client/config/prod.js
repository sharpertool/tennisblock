import merge from 'webpack-merge';

import baseConfigFunc from './base';
import {resolve} from "path";

export default ({env, options}) => {

  //console.log('Prod Options are ', options);
  console.log('Prod environment is ', env);

    const strategy = {
        'output.path': 'replace',
        'output.filename': 'replace',
    'output.publicPath': 'replace',
        'module.rules': 'append',
        'plugins': 'append',
    };

  const baseConfig = baseConfigFunc({env, options});

    var output = {
        filename: 'js/[name]_[hash].js',
    publicPath: `/static/`
  };

    return merge.strategy(strategy)(
        baseConfig,
        {
            output: output,
        }
  )
}
