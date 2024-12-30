import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './Activate.css';

function Activate() {
  const { uidb64, token } = useParams();
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const activateAccount = async () => {
      try {
        const response = await fetch(`http://localhost:8000/core/api/activate/${uidb64}/${token}/`, {
          method: 'GET',
        });
        setLoading(false);
        const data = await response.json();

        if (response.ok) {
          setMessage(data.message || 'Аккаунт успешно активирован! Перенаправление на страницу входа...');
          setTimeout(() => navigate('/login'), 3000);
        } else {
          setMessage(data.message || 'Ссылка активации недействительна или устарела.');
        }
      } catch (error) {
        setLoading(false);
        setMessage('Ошибка соединения с сервером. Проверьте интернет-соединение.');
      }
    };

    activateAccount();
  }, [uidb64, token, navigate]);

  return (
    <div className="activation-container">
      <div className="activation-card">
        <h2>Активация аккаунта</h2>
        {loading ? <p>Загрузка...</p> : <p>{message}</p>}
        <a href="/" className="back-link">Вернуться на главную</a>
      </div>
    </div>
  );
}

export default Activate;