import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {Row, Col, Input} from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
import styles from './styles.local.scss'

import SchedulePlayer from '~/components/SchedulePlayer/connected'
import ScheduledCouple from './ScheduledCouple'

const ScheduledCouples = (props) => {
  
  const {
    couples,
    guySubs, galSubs,
  } = props
  
  return (
    <>
      <Row className='d-sm-none d-m-block'>
        <Col xs={6} md={6} lg={6}>
          <h3 className={styles.tableHeader}>Guys</h3>
        </Col>
        <Col xs={12} md={6} lg={6}>
          <h3 className={styles.tableHeader}>Gals</h3>
        </Col>
      </Row>
      <Row>
        <Col>
          {couples.map((couple, index) => {
            return (
              <ScheduledCouple
                key={index} index={index}
                couple={couple}
                guySubs={guySubs} galSubs={galSubs}
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

