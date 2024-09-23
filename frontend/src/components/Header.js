import React from 'react';

function Header({ handleLogout }) {
  return (
    <header className="App-header">
      <h1>Welcome to Njål's Strava app</h1>
      <button className="logout-button" onClick={handleLogout}>Logout</button>
    </header>
  );
}

export default Header;