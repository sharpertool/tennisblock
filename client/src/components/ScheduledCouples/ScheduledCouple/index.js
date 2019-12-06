import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {Row, Col, Input} from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
import styles from './styles.local.scss'

import SchedulePlayer from '~/components/SchedulePlayer/connected'

const ScheduledCouple= (props) => {
  
  const {
    couple,
    index,
    guySubs, galSubs,
  } = props
  const {guy, gal} = couple
  
  return (
    <>
      <Row>
        <Col xs={12} md={6} lg={6}>
            <SchedulePlayer
              index={index}
              id={guy.id}
              player={guy}
              group='guys'
              subs={guySubs}
              altsubs={galSubs}
            />
        </Col>
        <Col xs={12} md={6} lg={6}>
            <SchedulePlayer
              index={index}
              id={gal.id}
              player={gal}
              group='gals'
              subs={galSubs}
              altsubs={guySubs}
            />
        </Col>
        <hr className="d-m-none d-xs-block"/>
      </Row>
    </>
  )
}

ScheduledCouple.propTypes = {
  guySubs: PropTypes.array,
  galSubs: PropTypes.array,
}

export default ScheduledCouple

