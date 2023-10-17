import React, { useState } from 'react';
import { apiRegisterUser } from '../Api/User'
// 在你的 Register.tsx 或相應的組件文件中

const Register: React.FC = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        nickname: '',
        password: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const formData = new FormData(e.target as HTMLFormElement);
        const data = Object.fromEntries(formData);
        apiRegisterUser(data);
    };

    return (
        <div>
            <h2>註冊</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Username" onChange={handleChange} />
                <input type="email" name="email" placeholder="Email" onChange={handleChange} />
                <input type="text" name="nickname" placeholder="Nickname" onChange={handleChange} />
                <input type="password" name="password" placeholder="Password" onChange={handleChange} />
                <button type="submit">註冊</button>
            </form>
        </div>
    );
};

export default Register;
