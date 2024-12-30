import React from 'react';
import { Helmet } from 'react-helmet';
import { Routes, Route } from 'react-router-dom';
import LoginForm from './components/auth/LoginForm';
import AdminDashboard from './components/auth/AdminDashboard';
import UserDashboard from './components/auth/UserDashboard';
import Signup from './components/auth/Signup';
import Activate from './components/Activate';
import HomePage from './components/HomePage';

function App() {
  return (
      <div className="App" style={{height: '100%', display: 'flex', flexDirection: 'column'}}>
        <header className="App-header">
          <Helmet>
            <title>AnimalCorePro</title>
          </Helmet>
          <Routes>
            <Route path="/" element={<HomePage/>}/>
            <Route path="/activate/:uidb64/:token" element={<Activate/>}/>
            <Route path="/login" element={<LoginForm/>}/>
              <Route path="/admin" component={AdminDashboard} />
              <Route path="/dashboard" component={UserDashboard} />
            <Route path="/register" element={<Signup/>}/>
          </Routes>
        </header>
      </div>
  );
}

export default App;
