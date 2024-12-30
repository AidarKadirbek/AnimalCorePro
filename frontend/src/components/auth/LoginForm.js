import React, { useState } from 'react';
import axios from 'axios';
import '../../App.css';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    try {
      const response = await axios.post('http://127.0.0.1:8000/core/api/login/', {
        username: formData.username,
        password: formData.password,
      });

      if (response.status === 200) {
        localStorage.setItem('token', response.data.token);
        
        if (response.data.status === 'staff') {
          setSuccessMessage('Авторизация успешна! Перенаправление в админку...');
          window.location.href = '/admin';
        } else {
          setSuccessMessage('Авторизация успешна! Перенаправление в ваш аккаунт...');
          window.location.href = '/dashboard';
        }
      } else {
        setError('Не удалось авторизоваться. Проверьте данные.');
      }
    } catch (error) {
      setError('Ошибка при подключении к серверу.');
    }
  };

  return (
    <div className="login-container">
      <h2>Авторизация</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Имя пользователя:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
          {error && <p className="error">{error}</p>}
        </div>
        <div>
          <label htmlFor="password">Пароль:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          {error && <p className="error">{error}</p>}
        </div>
        <button type="submit">Войти</button>
      </form>
      {successMessage && <p className="success">{successMessage}</p>}
    </div>
  );
};

export default LoginForm;