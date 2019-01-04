import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {Row, Col, Input} from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
import styles from './styles.local.scss'

class Couples extends Component {
  render() {
    const {couples, guySubs, galSubs, onPlayerChanged} = this.props
    const changes = []
    
    return (
      <React.Fragment>
        <Row>
          <Col xs={6}>
            <h3 className={styles.tableHeader}>Guys</h3>
          </Col>
          <Col xs={6}>
            <h3 className={styles.tableHeader}>Gals</h3>
          </Col>
        </Row>
        <Row>
          {couples.map((couple, index) => {
              const {guy, gal} = couple
              return (
                <React.Fragment key={index}>
                  <Col xs={12} md={6}>
                    <Input
                      type="select"
                      value={guy.id}
                      //className={changes[index].guy ? styles.changed : ''}
                      onChange={(e) => onPlayerChanged({
                        group: 'guys',
                        value: parseInt(e.target.value),
                        previous: guy.id
                      })}
                    >
                      <option value={guy.id}>{guy.name}</option>
                      {guySubs.map((s, i) => (
                        <option value={s.id} key={i}>{s.name}</option>
                      ))}
                    </Input>
                  </Col>
                  <Col xs={12} md={6}>
                    <Input
                      type="select"
                      value={gal.id}
                      //className={changes[index].gal ? styles.changed : ''}
                      onChange={(e) => onPlayerChanged({
                        group: 'gals',
                        value: parseInt(e.target.value),
                        previous: gal.id
                      })}
                    >
                      <option value={gal.id}>{gal.name}</option>
                      {galSubs.map((s, i) => (
                        <option value={s.id} key={i}>{s.name}</option>
                      ))}
                    </Input>
                  </Col>
                </React.Fragment>
              )
            }
          )
          }
        </Row>
      </React.Fragment>
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
  guySubs: PropTypes.array,
  galSubs: PropTypes.array,
}

export default Couples
