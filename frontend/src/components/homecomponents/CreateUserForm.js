import React, { useState } from 'react';
import { API_BASE_URL } from '../../Config';


function CreateUserForm({ onUserCreated }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showFailed, setShowFailed] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (password !== confirmPassword) {
            setErrorMessage("Passwords do not match.");
            setShowFailed(true);
            return;
        }

        const response = await fetch(`${API_BASE_URL}/api/createuser`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (data.status === 'success') {
            onUserCreated(username, password); // Pass credentials up to parent component
            localStorage.setItem('username', username);
            localStorage.setItem('isLoggedIn', 'true');
        } else {
            setErrorMessage(data.message || "Failed to create user.");
            setShowFailed(true);
        }
    };

    return (
        <form className="login-form" onSubmit={handleSubmit}>
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" value={username} onChange={e => setUsername(e.target.value)} />

            <label htmlFor="password">Password:</label>
            <input type="password" id="password" value={password} onChange={e => setPassword(e.target.value)} />

            <label htmlFor="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />

            <button type="submit" className='login-button'>Create User</button>

            {showFailed && <p style={{ color: 'red' }}>{errorMessage}</p>}
        </form>
    );
}

export default CreateUserForm;