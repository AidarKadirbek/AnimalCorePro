import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const UserDashboard = () => {
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userStatus = localStorage.getItem('status');

    if (!token || userStatus !== 'user') {
      navigate('/login');
      return;
    }

    if (token) {
      fetch('http://127.0.0.1:8000/core/api/user-info/', {
        headers: {
          'Authorization': `Token ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => setUserData(data));
    }
  }, [navigate]);

  if (!userData) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>User Dashboard</h1>
      <p>Welcome, {userData.username}!</p>
    </div>
  );
};

export default UserDashboard;