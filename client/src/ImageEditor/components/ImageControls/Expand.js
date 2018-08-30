import React, {Component} from 'react';
import {types} from '~/ImageEditor/modules/Modal';

class ExpandButton extends Component {
    handleZoom(e) {
        const {dispatch, dom_id} = this.props;
        dispatch({type: types.ZOOM_TOGGLE, dom_id});
    }
    
    render() {
        const {props, handleZoom} = this;
        return (
            <div className="row">
                <div className="col">
                    <div className="d-flex flex-row-reverse">
                        <a className="p-2"
                            href="javascript:void(0)"
                            onClick={handleZoom.bind(this)} className="expand-btn">
                            <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/t-1109/icon-expand.png" alt="expand"/>
                        </a>
                    </div>
                </div>
            </div>
        );
    }
}

export default ExpandButton;
