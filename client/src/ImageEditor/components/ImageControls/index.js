import React, {Component} from 'react';
import Zoom from './Zoom';
import Editor from './Editor';
import Download from './Download';

class ImageControls extends Component {
    render() {
        const {props} = this;
        return (
            <div className="row">
                <div className="col">
                    <div className="mx-auto card-links">
                        <Zoom {...props} />
                        <Editor {...props} />
                        <Download {...props} />
                        <a href="#" className="card-link">
                            <i className="fa fa-share"></i>
                        </a>
                    </div>
                </div>
            </div>
        );
    }
}

export default ImageControls;
