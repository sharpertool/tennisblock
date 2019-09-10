import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {Row, Col, Input} from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
import styles from './styles.local.scss'

class Couples extends Component {
  render() {
    const {couples} = this.props

    return (
      <>
        <Row>
          <Col xs={12} md={6} lg={6}>
            <h3 className={styles.tableHeader}>Guys</h3>
            {couples.map((couple, index) => {
              const { guy } = couple
              return (
                <div key={index} className="">
                  {guy.name}
                </div>
              )
            })}
          </Col>
          <Col xs={12} md={6} lg={6}>
            <h3 className={styles.tableHeader}>Gals</h3>

            {couples.map((couple, index) => {
              const { gal } = couple
              return (
                <div key={index} className="">
                  {gal.name}
                </div>
              )
            })}
          </Col>
        </Row>
      </>
    )
  }
}

Couples.propTypes = {
  couples: PropTypes.arrayOf(PropTypes.shape({
      guy: PropTypes.shape({
        id: PropTypes.number.isRequired,
      }).isRequired,
      gal: PropTypes.shape({
        id: PropTypes.number.isRequired,
      }).isRequired
    })
  ).isRequired,
}

export default Couples
