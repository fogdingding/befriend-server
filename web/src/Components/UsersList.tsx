// Components/UsersList.tsx
import React, { useEffect, useState } from 'react';
import { fetchUsersList } from '../Api/User';
import { Link } from 'react-router-dom'; 
import { Person } from '../Types/base';  
import { trackUser } from '../Api/User';

const UsersList: React.FC = () => {
  const [users, setUsers] = useState<Person[]>([]);
  const handleUserClick = async (userId: number | null) => {
    if (userId === null) {
        console.error('User ID is null');
        return;
    }
    try {
        await trackUser(userId);
    } catch (error) {
        console.error('Error tracking user:', error);
    }
};
  useEffect(() => {
    const getUsers = async () => {
      try {
        const userList = await fetchUsersList();
        setUsers(userList);
      } catch (error) {
        console.error('Error fetching users list:', error);
      }
    };

    getUsers();
  }, []);

  return (
    <div>
      <h1>所有用戶</h1>
      <ul>
        {users.map(user => (
          <li key={user.user_id}>
            {user.username} 
            <Link to={`/profile/${user.user_id}`} onClick={() => handleUserClick(user.user_id)}>查看詳細</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UsersList;
