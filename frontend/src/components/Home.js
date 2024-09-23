import React, { useEffect, useState } from 'react';
import LoginForm from './homecomponents/LoginForm';
import CredentialsDisplay from './homecomponents/CredentialsDisplay';
import StartScreen from './homecomponents/StartScreen';
import LoginFailed from './homecomponents/LoginFailed';
import CreateUserForm from './homecomponents/CreateUserForm';
import DescriptionDisplay from './homecomponents/DescriptionDisplay';
import { API_BASE_URL } from '../Config';

const AppState = {
    INITIAL: 'INITIAL',
    ABOUT_TO_LOG_IN: 'ABOUT_TO_LOG_IN',
    LOGIN_FAILED: 'LOGIN_FAILED',
    CREATE_USER: 'CREATE_USER',
    CREDENTIALS_DISPLAYED: 'CREDENTIALS_DISPLAYED',
    WRITE_DESCRIPTION: 'WRITE_DESCRIPTION'
};

function Home() {
    const [message, setMessage] = useState(''); 
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const [appState, setAppState] = useState(AppState.INITIAL);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [authorized, setAuthorized] = useState(false);

    useEffect(() => {
        const loggedIn = localStorage.getItem('isLoggedIn');
        const authorized = localStorage.getItem('authorized');
        if (loggedIn === 'true') {
            const username = localStorage.getItem('username');
            setCredentials({ username : username, password: '' });
            setAppState(AppState.CREDENTIALS_DISPLAYED);
            if (authorized === 'true') {
                setAuthorized(true);
                setAppState(AppState.WRITE_DESCRIPTION);
            }
        }
    }
    , []);

    const handleLoginClick = () => {
        if (isLoggedIn) {
            setAppState(AppState.CREDENTIALS_DISPLAYED);
        }
        setAppState(AppState.ABOUT_TO_LOG_IN);
    };

    const handleCreateAccount = () => {
        setAppState(AppState.CREATE_USER);
    };

    const handleUserCreated = (username, password) => {
        setCredentials({ username, password });
        setAppState(AppState.CREDENTIALS_DISPLAYED);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const usernameInput = event.target.username.value;
        const passwordInput = event.target.password.value;

        const response = await fetch(`${API_BASE_URL}/api/senduserdata`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: usernameInput, password: passwordInput })
        });

        const data = await response.json();
        setMessage(data.message);

        if (data.status === 'success') {
            setAppState(AppState.CREDENTIALS_DISPLAYED);
            setCredentials({ username: usernameInput, password: passwordInput });
            localStorage.setItem('username', usernameInput);
            localStorage.setItem('isLoggedIn', 'true');
            if (data.haveAuthorized === "yes") {
                setAuthorized(true);
                localStorage.setItem('authorized', 'true');
                setAppState(AppState.WRITE_DESCRIPTION);
            }
        } else {
            setAppState(AppState.LOGIN_FAILED);
        }
    };

    const handleRetry = () => {
        setMessage('');
        setAppState(AppState.ABOUT_TO_LOG_IN);
    };

    return (
        <div className="Home">
            {appState === AppState.INITIAL && (
                <StartScreen handleLoginClick={handleLoginClick}  />
            )}
            {appState === AppState.ABOUT_TO_LOG_IN && (
                <LoginForm handleSubmit={handleSubmit} handleCreateAccount={handleCreateAccount}/>
            )}
            {appState === AppState.CREATE_USER && (
                <CreateUserForm onUserCreated={handleUserCreated} />
            )}
            { appState === AppState.CREDENTIALS_DISPLAYED && (
                <CredentialsDisplay username={credentials.username} message={message} />
            )}
            {appState === AppState.LOGIN_FAILED && (
                <LoginFailed onRetry={handleRetry} />
            )}
            {appState === AppState.WRITE_DESCRIPTION && (
                <DescriptionDisplay />
            )}
            
            <img src="/megsykler.png" alt="Cycling" className="user-image" />
        </div>
    );
}

export default Home;