import React, { useState } from 'react';
import { apiLogin } from '../Api/User'

const Login: React.FC = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [showModal, setShowModal] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const { username, password } = formData;
        try {
            const status = await apiLogin(username, password);
            setShowModal(status);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <h2>登入</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Username" onChange={handleChange} />
                <input type="password" name="password" placeholder="Password" onChange={handleChange} />
                <button type="submit">登入</button>
            </form>

            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        <span onClick={() => setShowModal(false)}>&times;</span>
                        <p>登入成功！</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Login;
