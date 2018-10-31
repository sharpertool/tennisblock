import React from 'react'
import Proptypes from 'prop-types'
import {Provider} from 'react-redux'

import MatchReview from '~/containers/MatchReview'

const matchreview = ({store}) => {
  return (
    <Provider store={store}>
      <MatchReview/>
    </Provider>)
}

matchreview.propTypes = {
}


export default matchreview
