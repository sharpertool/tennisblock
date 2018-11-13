import React, { Component } from 'react'
import classes from './styles.local.scss'
import SocialButtons from '~/components/SocialButtons'
import LoginForm from '~/components/Login'

class Home extends Component {
    render() {
        return (
            <div className={classes.Home}>
                <SocialButtons/>

                <div className={['container', classes.LoginContainer].join(' ')}>
                    <div className="text-center">
                        <img src="/static/img/dummy-logo.png" className="mb-5"/>
                        <p className="mt-3 mb-5">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusantium aperiam autem dolorem doloremque dolorum earum expedita fugiat impedit in ipsum iste iure, laborum libero minus nobis tempora totam, ullam velit?</p>
                    </div>

                    <LoginForm/>

                    <p className="text-center mt-4">&copy; 2018 TennisBlock.com</p>
                </div>
            </div>
        )
    }
}

export default Home