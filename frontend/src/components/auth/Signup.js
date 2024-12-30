import React, { useState } from 'react';
import axios from 'axios';
import '../../App.css';

const Signup = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
    });

    const [errors, setErrors] = useState({});
    const [successMessage, setSuccessMessage] = useState('');

    const validateEmail = (email) => /\S+@\S+\.\S+/.test(email);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors({});
        setSuccessMessage('');

        if (!validateEmail(formData.email)) {
            setErrors({ email: 'Введите корректный email.' });
            return;
        }

        if (formData.password !== formData.confirmPassword) {
            setErrors({ confirmPassword: 'Пароли не совпадают' });
            return;
        }

        try {
            const response = await axios.post('http://127.0.0.1:8000/core/api/register/', {
                username: formData.username,
                email: formData.email,
                password: formData.password,
                confirm_password: formData.confirmPassword,
            });

            if (response.status === 201 || response.status === 200) {
                setSuccessMessage('Регистрация прошла успешно! Проверьте вашу почту для активации аккаунта.');
                setFormData({
                    username: '',
                    email: '',
                    password: '',
                    confirmPassword: '',
                });
            } else {
                setErrors({ non_field_errors: 'Не удалось зарегистрироваться. Проверьте данные.' });
            }
        } catch (error) {
            if (error.response && error.response.data) {
                setErrors(error.response.data);
            } else {
                console.error('Ошибка:', error);
                setErrors({ non_field_errors: 'Ошибка при подключении к серверу.' });
            }
        }
    };

    return (
        <div className="signup-container">
            <h2>Регистрация</h2>
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
                    {errors.username && <p className="error">{errors.username}</p>}
                </div>
                <div>
                    <label htmlFor="email">Электронная почта:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                    {errors.email && <p className="error">{errors.email}</p>}
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
                    {errors.password && <p className="error">{errors.password}</p>}
                </div>
                <div>
                    <label htmlFor="confirmPassword">Подтвердите пароль:</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        required
                    />
                    {errors.confirmPassword && <p className="error">{errors.confirmPassword}</p>}
                </div>
                {errors.non_field_errors && (
                    <p className="error">{errors.non_field_errors}</p>
                )}
                <button type="submit">Зарегистрироваться</button>
            </form>
            {successMessage && <p className="success">{successMessage}</p>}
        </div>
    );
};

export default Signup;