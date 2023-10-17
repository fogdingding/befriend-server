import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Register from './Components/Register';
import Login from './Components/Login';
import Profile from './Components/Profile';
import UsersList from './Components/UsersList';
import WhoCheckedMe from './Components/WhoCheckedMe';

const App: React.FC = () => {
    return (
        <Router>
            <div>
                <nav>
                    <ul>
                        <li>
                            <Link to="/register">註冊</Link>
                        </li>
                        <li>
                            <Link to="/login">登入</Link>
                        </li>
                        <li>
                            <Link to="/profile">簡介</Link>
                        </li>
                        <li>
                            <Link to="/userlist">查看現有用戶</Link>
                        </li>
                        <li>
                            <Link to="/whocheckedme">查看誰查看過我</Link>
                        </li>
                    </ul>
                </nav>

                <Routes>
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/profile/:user_id?" element={<Profile />} />
                    <Route path="/userlist" element={<UsersList />} />
                    <Route path="/whocheckedme" element={<WhoCheckedMe />} />
                    <Route path="/" element={<div>Welcome to Friend Website!</div>} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
