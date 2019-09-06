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
} from '~/pages/Schedule/modules'
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

import CouplesEditor from '~/components/CouplesEditor'

const girls = [
  {id: 0, first: 'Vicki', last: 'Henderson', gender: 'f'},
  {id: 1, first: 'Lynn', last: 'Kirshaw', gender: 'f'},
  {id: 2, first: 'Stacy', last: 'Jones', gender: 'f'},
  {id: 3, first: 'Sue', last: 'Carney', gender: 'f'},
  {id: 4, first: 'Veronica', last: 'Mars', gender: 'f'},
  {id: 5, first: 'Lisa', last: 'Bettis', gender: 'f'},
  {id: 6, first: 'Kristine', last: 'Kittleson', gender: 'f'},
  {id: 7, first: 'Ellen', last: 'Quinn', gender: 'f'},
]

const guys = [
  {id: 10, first: 'Ed', last: 'Henderson', gender: 'm'},
  {id: 11, first: 'Fred', last: 'Wolins', gender: 'm'},
  {id: 12, first: 'Rick', last: 'Jones', gender: 'm'},
  {id: 13, first: 'Matt', last: 'Carney', gender: 'm'},
  {id: 14, first: 'Dave', last: 'Bettis', gender: 'm'},
  {id: 15, first: 'Randy', last: 'Staufer', gender: 'm'},
  {id: 16, first: 'Brian', last: 'Kittleson', gender: 'm'},
  {id: 17, first: 'Oscar', last: 'Martinez', gender: 'm'},
]

storiesOf('Couples Editor', module)
  .addDecorator(story => <Provider story={story()}/>)
  .add('Couples Editor', () => (
    <CouplesEditor girls={girls} guys={guys}/>
  ))
