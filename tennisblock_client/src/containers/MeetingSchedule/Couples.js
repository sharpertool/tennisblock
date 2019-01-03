import React, { Component } from 'react'
import { Row, Col, Input } from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
import styles from './styles.local.scss'

class Couples extends Component {
  render() {
    const { blockplayers, match,
            guySubs, galSubs, changes, changeBlockPlayer
    } = this.props

    const couples = blockplayers.couples ? blockplayers.couples : []

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
                      className={changes[index].guy ? styles.changed : ''}
                      onChange={(e) => changeBlockPlayer({
                        value: parseInt(e.target.value),
                        gender: 'guy',
                        key: index
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
                      value={guy.id}
                      className={changes[index].gal ? styles.changed : ''}
                      onChange={(e) => changeBlockPlayer({
                        value: parseInt(e.target.value),
                        gender: 'gal',
                        key: index
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

export default Couples
