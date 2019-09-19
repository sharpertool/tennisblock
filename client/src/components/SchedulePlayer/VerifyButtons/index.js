import React from 'react'
import PropTypes from 'prop-types'

// Display if code is N, A
const VerifyButtons = ({
                         id,
                         vcode,
                         onSendVerify,
                         onManualVerify,
                       }) => {
  
  const show = vcode == 'N' || vcode == 'A'
  
  const msg = vcode == 'A' ? 'Re-Notify' : 'Notify'
  
  if (show) {
    return (
      <>
        <button onClick={() => onSendVerify(id)}>
          {msg}
        </button>
        <button onClick={() => onManualVerify(id)}>
          Verify
        </button>
      </>
    )
  }
  return null
}

VerifyButtons.propTypes = {}

export default VerifyButtons