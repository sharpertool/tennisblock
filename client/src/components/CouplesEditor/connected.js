import React from 'react'
import {connect} from 'react-redux'
import {selectors, actions} from '~/redux-page'

import CouplesEditor from './index'

const connectedComponent = ({
                              guys,
                              girls,
                              couples,
                              addCouple,
                              removeCouple,
                              updateSingles,
                              updateFulltime,
                              updateName,
                            }) => {
  return (
    <CouplesEditor
      guys={guys}
      girls={girls}
      couples={couples}
      addCouple={addCouple}
      removeCouple={removeCouple}
      updateSingles={updateSingles}
      updateFulltime={updateFulltime}
      updateName={updateName}
    />
)
}

const mapStateToProps = (state) => {
  return {
    guys: selectors['season:getGuys'](state),
    girls: selectors['season:getGirls'](state),
    couples: selectors['season:getCouples'](state),
  }
}

const dispatchActions = {
  addCouple: actions['season:addCouple'],
  removeCouple: actions['season:removeCouple'],
  updateSingles: actions['season:coupleChangeSingles'],
  updateFulltime: actions['season:coupleChangeFulltime'],
  updateName: actions['season:coupleChangeName'],
}

export default connect(mapStateToProps, dispatchActions)(connectedComponent)
