import React from 'react'
import {Provider} from 'react-redux'

import BlockMembersTable from '~/components/BlockMembersTable/connected'

const root = ({store}) => {
  
  return (
    <Provider store={store}>
      <div className={'dynamic'}>
        <h3>Block Members - React</h3>
        <BlockMembersTable/>
      </div>
    </Provider>)
}

export default root
