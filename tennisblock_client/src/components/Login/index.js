import React, { Component } from 'react'
import classes from './styles.local.scss'

class Login extends Component {
    render() {
        return (
            <div className={classes.LoginForm}>
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
        )
    }
}

export default Login