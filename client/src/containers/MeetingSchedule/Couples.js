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
      <>
        <Row>
          <Col xs={12} md={6} lg={6}>
            <h3 className={styles.tableHeader}>Guys</h3>
            {couples.map((couple, index) => {
              const { guy } = couple
              return (
                <div key={index} className="form-group">
                  <Input
                    type="select"
                    value={guy.id}
                    //className={changes[index].guy ? styles.changed : ''}
                    onChange={(e) => onPlayerChanged({
                      group: 'guys',
                      index: index,
                      value: parseInt(e.target.value),
                      previous: guy.id
                    })}
                  >
                    <option
                      value={guy.id}>
                      {guy.name}
                    </option>
                    <option
                      value={-1}>
                      {'---'}
                    </option>
                    {guySubs.map((s, i) => (
                      <option
                        value={s.id} key={i}>
                        {s.name}
                      </option>
                    ))}
                    <option
                      value={-1}>
                      {'---'}
                    </option>
                    {galSubs.map((s, i) => (
                      <option
                        value={s.id} key={100+i}>
                        {s.name}
                      </option>
                    ))}
                  </Input>
                </div>
              )
            })}
          </Col>
          <Col xs={12} md={6} lg={6}>
            <h3 className={styles.tableHeader}>Gals</h3>

            {couples.map((couple, index) => {
              const { gal } = couple
              return (
                <div key={index} className="form-group">
                  <Input
                    type="select"
                    value={gal.id}
                    //className={changes[index].gal ? styles.changed : ''}
                    onChange={(e) => onPlayerChanged({
                      group: 'gals',
                      index: index,
                      value: parseInt(e.target.value),
                      previous: gal.id
                    })}
                  >
                    <option
                      value={gal.id}>
                      {gal.name}
                    </option>
                    <option
                      value={-1}>
                      {'---'}
                    </option>
                    {galSubs.map((s, i) => (
                      <option
                        value={s.id} key={i}>
                        {s.name}
                      </option>
                    ))}
                    <option
                      value={-1}>
                      {'---'}
                    </option>
                    {guySubs.map((s, i) => (
                      <option
                        value={s.id} key={100+i}>
                        {s.name}
                      </option>
                    ))}
                  </Input>
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
  guySubs: PropTypes.array,
  galSubs: PropTypes.array,
}

export default Couples
