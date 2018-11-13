import React, { Component } from 'react'
import classes from './styles.local.scss'

class SocialButtons extends Component {
    render() {
        return (
            <ul className={classes.SocialButtons}>
                <li>
                    <i className="fa fa-facebook-square fa-2x"></i>
                </li>
                <li>
                    <i className="fa fa-twitter-square fa-2x"></i>
                </li>
                <li className={classes.SocialDivider}></li>
                <li>
                    <i className="fa fa-envelope-o fa-2x"></i>
                </li>
            </ul>
        )
    }
}

export default SocialButtons