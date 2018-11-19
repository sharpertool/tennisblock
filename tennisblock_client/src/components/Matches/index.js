import { connect } from 'react-redux'
import React, { Component } from 'react'

import { getBlockPlayers } from '~/Schedule/modules/teams/actions'

class Matches extends Component {
  componentDidMount() {
    const { match, getBlockPlayers } = this.props
    const { params } = match
    if(match) {
      console.log(params)
      getBlockPlayers(params.id)
    }
  }
  render() {
    const { blockplayers } = this.props
    return(
      <div className="matches">{blockplayers && blockplayers.couples.map((couple, index) => (
        <div key={index}>{couple.gal.name} {couple.guy.name}</div>
      ))}</div>
    )
  }
}

const mapStateToProps = ({ teams }) => {
  const { blockplayers } = teams
  return {
    blockplayers
  }
}

const mapDispatchToProps = {
  getBlockPlayers
}



export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Matches)
