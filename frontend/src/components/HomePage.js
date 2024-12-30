import React from 'react';
import './HomePage.css';

function HomePage() {
  return (
    <div className="homepage-container">
      <header className="homepage-header">
        <h1>Добро пожаловать в AnimalCorePro</h1>
        <p>Система управления учётом животных</p>
      </header>
      <section className="homepage-content">
        <div className="card">
          <h2>Войти в систему</h2>
          <p>Контролируйте систему, управляйте пользователями и следите за базой данных.</p>
          <a href="/login" className="homepage-link">Войти</a>
        </div>
        <div className="card">
          <h2>Регистрация</h2>
          <p>Создайте аккаунт, чтобы начать работу с системой.</p>
          <a href="/register" className="homepage-link">Регистрация</a>
        </div>
      </section>
      <footer className="homepage-footer">
        <p>&copy; 2024 AnimalCorePro. Все права защищены.</p>
      </footer>
    </div>
  );
}

export default HomePage;