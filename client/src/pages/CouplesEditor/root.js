import React from 'react'
import ReactDOM from 'react-dom'
import {Provider} from 'react-redux'

import CouplesEditor from '~/components/CouplesEditor/connected'

const root = ({store, elements}) => {
  
  return (
    <Provider store={store}>
      <CouplesEditor>
      </CouplesEditor>
    </Provider>
  )
}

export default root
