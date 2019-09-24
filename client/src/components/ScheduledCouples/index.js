import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {Row, Col, Input} from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
import styles from './styles.local.scss'

import SchedulePlayer from '~/components/SchedulePlayer/connected'

const ScheduledCouples = (props) => {
  
  const {
    couples,
    guySubs, galSubs,
  } = props
  
  return (
    <>
      <Row>
        <Col xs={12} md={6} lg={6}>
          <h3 className={styles.tableHeader}>Guys</h3>
          {couples.map((couple, index) => {
            const {guy} = couple
            return (
              <SchedulePlayer
                key={index}
                index={index}
                id={guy.id}
                player={guy}
                group='guys'
                subs={guySubs}
                altsubs={galSubs}
              />
            )
          })}
        </Col>
        <Col xs={12} md={6} lg={6}>
          <h3 className={styles.tableHeader}>Gals</h3>
          
          {couples.map((couple, index) => {
            const {gal} = couple
            return (
              <SchedulePlayer
                key={index}
                index={index}
                id={gal.id}
                player={gal}
                group='gals'
                subs={galSubs}
                altsubs={guySubs}
              />
            )
          })}
        </Col>
      </Row>
    </>
  )
}

ScheduledCouples.propTypes = {
  couples: PropTypes.arrayOf(PropTypes.shape({
      guy: PropTypes.shape({
        id: PropTypes.number.isRequired,
      }).isRequired,
      gal: PropTypes.shape({
        id: PropTypes.number.isRequired,
      }).isRequired
    })
  ).isRequired,
  guySubs: PropTypes.array,
  galSubs: PropTypes.array,
}

export default ScheduledCouples

