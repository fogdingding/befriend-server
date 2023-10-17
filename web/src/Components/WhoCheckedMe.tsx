// Components/WhoCheckedMe.tsx
import React, { useEffect, useState } from 'react';
import { fetchWhoCheckedMe } from '../Api/User';
import { Person } from '../Types/base';

const WhoCheckedMe: React.FC = () => {
  const [users, setUsers] = useState<Person[]>([]);

  useEffect(() => {
    const getCheckers = async () => {
      try {
        const userList = await fetchWhoCheckedMe();
        setUsers(userList);
      } catch (error) {
        console.error('Error fetching who checked me list:', error);
      }
    };

    getCheckers();
  }, []);

  return (
    <div>
      <h1>查看過我的用戶</h1>
      <ul>
        {users.map(user => (
          <li key={user.user_id}>
            {user.username} 
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WhoCheckedMe;
