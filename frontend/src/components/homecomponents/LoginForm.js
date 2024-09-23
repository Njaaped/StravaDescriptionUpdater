import React from 'react';

function LoginForm({ handleSubmit, handleCreateAccount }) {
    return (
        <div>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="username">Username:</label>
                <input type="text" id="username" name="username" />
                <label htmlFor="password">Password:</label>
                <input type="password" id="password" name="password" />
                <button type="submit" className="login-button">Submit</button>
            </form>
            <p style={{ marginTop: '20px', textAlign: 'center' }}>
                Don't have a user? 
                <button onClick={handleCreateAccount} className='login-button'>
                    Create User
                </button>
            </p>
        </div>
    );
}

export default LoginForm;