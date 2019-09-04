import React from 'react'
import {storiesOf} from '@storybook/react'
import {action} from '@storybook/addon-actions'
import {common_options} from '../common_options'
import merge from 'webpack-merge'

import {comments, comments_gen} from './all_comments'

export const moduleConfig = {
  axios_config: {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
  },
}

import {
  selectors,
  actions,
  rootSaga,
  rootReducer,
  set_config, initialize
} from '~/pages/SchedulePage/modules'
import {makeStore, mockAxios} from '../stories_utils'

import mkProvider from '../provider'
import {addMocks} from './api_mock'

const maxios = mockAxios()
addMocks(maxios)

moduleConfig.selectors = selectors

const options = merge(common_options, {
  coupleseditor_opts: {
    page_url: '/garden/this_garden', //'{{ request.path }}',
    // Put placeholders in for the values that must be supplied by client
    // Syntax indicates expected type
    query_url: '/talk/api/comments/str:group/slug:page/',
    add_url: '/talk/api/comments/str:group/slug:page/',
    reply_url: '/talk/api/comments/str:group/slug:page/int:id/',
    delete_url: '/talk/api/comments/str:group/slug:page/int:id/',
    initial_state: {
    }
  },
})

set_config({defaults: moduleConfig, options: options})

initialize(options)
//import configureStore from './store'
//const store = configureStore(null, null)

// Create the store
const store = makeStore({
  rootSaga: rootSaga,
  rootReducer: rootReducer,
  options: options
}, {name: 'Couples Editor'})

const Provider = mkProvider(store)

storiesOf('Couples Editor', module)
  .addDecorator(story => <Provider story={story()}/>)
