import React, { Component } from 'react'
import { connect } from 'react-redux'
import Breadcrumb from '~/components/ui/Breadcrumb'
import { selectors } from '~/Schedule/modules'


class ScheduleContainer extends Component {
  render() {
    return (
      <div className="schedule-layout">
        <Breadcrumb {...this.props}/>
        <main>
          {this.props.children}
        </main>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    blockplayers: selectors.getBlockPlayers(state)
  }
}

export default connect(
  mapStateToProps
)(ScheduleContainer)
