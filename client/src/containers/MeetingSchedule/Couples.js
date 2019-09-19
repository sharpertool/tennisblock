import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {connect} from 'react-redux'
import {Row, Col, Input} from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
import styles from './styles.local.scss'
import {actions, selectors} from '~/redux-page'

const Couples = (props) => {
  
  const {
    couples,
    guySubs, galSubs,
    onPlayerChanged,
    verifyStatus,
    verifyPlayer,
    notifyPlayer,
  } = props
  const changes = []
  
  const onSendVerify = (id) => {
    console.log(`Send verification to ${id}`)
    notifyPlayer({id: id})
  }
  
  const onManualVerify = (id) => {
    console.log(`Manually verify id ${id}`)
    verifyPlayer({id: id})
  }
  
  const buttons = (vcode, id) => {
    switch (vcode) {
      case 'N':
        return (
          <>
            <button onClick={() => onSendVerify(id)}>Send Verification Request</button>
            <button onClick={() => onManualVerify(id)}>Verify</button>
          </>
        
        )
      case 'A':
        return (
          <>
            <button onClick={() => onSendVerify(id)}>re-send Verification Request</button>
            <button onClick={() => onManualVerify(id)}>Verify</button>
          </>
        )
      default:
        return null
    }
  }
  
  return (
    <>
      <Row>
        <Col xs={12} md={6} lg={6}>
          <h3 className={styles.tableHeader}>Guys</h3>
          {couples.map((couple, index) => {
            const {guy} = couple
            const vcode = verifyStatus[guy.id]
            return (
              <div key={index} className="form-group">
                <Input
                  type="select"
                  className={vcode == 'C'
                    ? styles.verified
                    : vcode == 'R' ?
                      styles.rejected
                      : vcode == 'A' ? styles.awaiting : null}
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
                      value={s.id} key={100 + i}>
                      {s.name}
                    </option>
                  ))}
                </Input>
                {buttons(vcode, guy.id)}
              </div>
            )
          })}
        </Col>
        <Col xs={12} md={6} lg={6}>
          <h3 className={styles.tableHeader}>Gals</h3>
          
          {couples.map((couple, index) => {
            const {gal} = couple
            const vcode = verifyStatus[gal.id]
            return (
              <div key={index} className="form-group">
                <Input
                  type="select"
                  value={gal.id}
                  className={vcode == 'C'
                    ? styles.verified
                    : vcode == 'R' ?
                      styles.rejected
                      : vcode == 'A' ? styles.awaiting : null}
                  //className={changes[index].gal ? styles.changed : ''}
                  onChange={(e) => onPlayerChanged({
                    group: 'gals',
                    index: index,
                    value: parseInt(e.target.value),
                    previous: gal.id
                  })}
                >
                  <option
                    value={gal.id}
                  >
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
                      value={s.id} key={100 + i}>
                      {s.name}
                    </option>
                  ))}
                </Input>
                {buttons(vcode, gal.id)}
              </div>
            )
          })}
        </Col>
      </Row>
    </>
  )
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

const mapStateToProps = (state) => {
  return {
  
  }
}

console.dir(actions)
const mapDispatchToProps = {
  verifyPlayer: actions['schedule:manualVerifyPlayer'],
  notifyPlayer: actions['schedule:notifyPlayer'],
}

export default connect(mapStateToProps, mapDispatchToProps)(Couples)
