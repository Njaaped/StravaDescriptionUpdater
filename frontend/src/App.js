import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import './Header.css';
import './Footer.css';
import './Home.css';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import StravaCallback from './components/StravaCallback';
import dotenv from 'dotenv';


function App() {
  const [homeKey, setHomeKey] = useState(0);  

  dotenv.config();

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('username');
    localStorage.removeItem('authorized');
    setHomeKey(prevKey => prevKey + 1);  // Reset Home component on logout
  };

  return (
    <div className="App">
      <Router>
        <Header handleLogout={handleLogout} />
        <Routes>
          <Route path="/callback" element={<StravaCallback />} />
          <Route path="/" element={<Home key={homeKey} />} />
        </Routes>
        <Footer />
      </Router>
    </div>
  );
}

export default App;