import React, { Component } from 'react'
import classes from './styles.local.scss'

class Home extends Component {
    render() {
        return (
            <div className={classes.Home}>
                <ul className={classes.Head}>
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

                <div className={['container', classes.LoginContainer].join(' ')}>
                    <div className="text-center">
                        <img src="/static/img/dummy-logo.png" className="mb-5"/>
                        <p className="mt-3 mb-5">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusantium aperiam autem dolorem doloremque dolorum earum expedita fugiat impedit in ipsum iste iure, laborum libero minus nobis tempora totam, ullam velit?</p>
                    </div>
                    <div className={classes.FormBox}>
                        <div className="form-group">
                            <input type="text" className={['form-control', classes.InputFields].join(' ')} placeholder="Username"/>
                        </div>
                        <div className="form-group">
                            <input type="password" className={['form-control', classes.InputFields].join(' ')} placeholder="Password"/>
                        </div>

                        <a href="#" className={classes.ForgotPasswordLink}>Forgot Password?</a>

                        <div className="row">
                            <div className="col-7">
                                <div className="form-group form-check mb-0 pt-2">
                                    <input type="checkbox" className="form-check-input" id="remember"/>
                                    <label className="form-check-label text-white" htmlFor="remember">Remember me</label>
                                </div>
                            </div>
                            <div className="col-5">
                                <button type="button" className="btn btn-danger btn-lg btn-block">Log In</button>
                            </div>
                        </div>
                    </div>

                    <p className="text-center mt-4">&copy; 2018 TennisBlock.com</p>
                </div>
            </div>
        )
    }
}

export default Home