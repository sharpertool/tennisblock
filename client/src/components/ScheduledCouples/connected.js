import React, {Component} from 'react'
import {connect} from 'react-redux'
import {actions, selectors} from '~/redux-page'

import Couples from './index'

const mapStateToProps = (state) => {
  return {
    guySubs: selectors.getGuySubs(state),
    galSubs: selectors.getGalSubs(state),
  }
}

console.dir(actions)
const mapDispatchToProps = {
}

export default connect(mapStateToProps, mapDispatchToProps)(Couples)
