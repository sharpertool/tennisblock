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
} from '~/pages/StoriesTestingPage/modules'
import {makeStore, mockAxios} from '../stories_utils'

import mkProvider from '../provider'
import {addMocks} from './api_mock'

const maxios = mockAxios()
addMocks(maxios)

moduleConfig.selectors = selectors

const options = merge(common_options, {
  tronictalk_opts: {
    enabled: true,
    use_draftail: true,
    channel_path: '',
    channels_config_url: '', //'{% url "tronictalk:config" %}',
    page_url: '/garden/this_garden', //'{{ request.path }}',
    page_slug: 'this_garden', //'{{ page.slug }}',
    page_id: 28, // '{{ page.pk }}',
    // Put placeholders in for the values that must be supplied by client
    // Syntax indicates expected type
    query_url: '/talk/api/comments/str:group/slug:page/',
    add_url: '/talk/api/comments/str:group/slug:page/',
    reply_url: '/talk/api/comments/str:group/slug:page/int:id/',
    delete_url: '/talk/api/comments/str:group/slug:page/int:id/',
    initial_state: {
      comments: comments,
      use_draftail: true,
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
}, {name: 'Search Dialog'})

const Provider = mkProvider(store)

import CommentHeader from '~/components/TreeComments/CommentHeader'
import CommentItem from '~/components/TreeComments/CommentList/CommentItem/connected'
import CommentList from '~/components/TreeComments/CommentList/connected'
import CommentForm from '~/components/TreeComments/CommentForm'
import CommentsContainer from '~/components/TreeComments'

storiesOf('Gardentronic Comment', module)
  .addDecorator(story => <Provider story={story()}/>)
  .add('CommentHeader', () => {
    return (
      <div>
        <CommentHeader onNewCommentClick={() => {
        }}/>
      </div>
    )
  })
  .add('Comment', () => {
    return (
      <div>
        <CommentItem
          id={1}
          replies={[]}
          addComment={() => {}}
        />
      </div>
    )
  })
  .add('Comment with replies', () => {
    return (
      <div>
        <CommentItem
          id={1}
          replies={[
            {id: 2, children: []},
            {
              id: 6, children: [
                {id: 4, children: []},
              ]
            },
          ]
          }
          addComment={() => {}}
        />
      </div>
    )
  })
  .add('CommentForm', () => {
    return (
      <div>
        <CommentForm addCommentOrReply={() => {
        }}/>
      </div>
    )
  })
  .add('Comment List', () => {
    return (
      <div>
        <CommentList
          comments={comments_gen}
          addComment={() => {}}
        />
      </div>
    )
  })
  .add('Nested Comment List', () => {
    return (
      <div>
        <CommentList
          comments={comments_gen}
          addComment={() => {}}
        />
      </div>
    )
  })
  .add('Comments Complete Section', () => {
    return (
      <div>
        <CommentsContainer
          comments={comments_gen}
          addComment={action('add comment')}
          mode={'desktop'}
        />
      </div>
    )
  })
  .add('Comments Complete Section Mobile', () => {
    return (
      <div>
        <CommentsContainer
          comments={comments_gen}
          addComment={action('add comment')}
          mode={'mobile'}
        />
      </div>
    )
  })
