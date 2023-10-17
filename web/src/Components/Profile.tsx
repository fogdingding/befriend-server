

import React, { useEffect, useState } from 'react';
import { fetchProfileData, updateProfileData } from '../Api/User';
import { Person } from '../Types/base';
import { useParams } from 'react-router-dom';

interface Props {
  userId?: string;
}

const MyProfile: React.FC<Props> = ({ userId }) => {
  const { user_id } = useParams<{ user_id: string }>();
  const [userData, setUserData] = useState<Person | null>(null);
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [editedData, setEditedData] = useState<Omit<Person, 'user_id'> | null>(null);

  useEffect(() => {
    const fetchAndSetUserData = async () => {
      let id: any;
      if (user_id) {
        id = user_id;
      } else {
        const userItem = sessionStorage.getItem('user');
        if (!userItem) {
          console.error('User data not found in sessionStorage');
          return;
        }
        const user_data: Person = JSON.parse(userItem);
        id = user_data.user_id;
      }
  
      if (id) {
        try {
          const data = await fetchProfileData(id);
          setUserData(data[0]); 
        } catch (error) {
          console.error('Error fetching user data:', error);
        }
      }
    };
  
    fetchAndSetUserData();
  },  [userId, user_id]);
  
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setEditedData(prev => {
        if (prev) {
          return {
            ...prev,
            [name]: value
          };
        }
        return {
            username: "",
            email: "",
            nickname: "",
            password: null,
            img: "",
            self_name: "",
            first_name: "",
            last_name: "",
            introduction: "",
            interest: ""
          };
      });
  };

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e: ProgressEvent<FileReader>) => {
        if (e.target?.result) {
            const imgString = e.target.result as string;
            setEditedData(prev => {
                if (prev) {
                    return {
                        ...prev,
                        img: imgString
                    };
                }
                return {
                    username: "",
                    email: "",
                    nickname: "",
                    password: null,
                    img: "",
                    self_name: "",
                    first_name: "",
                    last_name: "",
                    introduction: "",
                    interest: ""
                };
            });
        }
    };
    reader.readAsDataURL(file);
    }
};


    const handleEditSubmit = async () => {
        if (editedData) {
            try {
                const updatedData = await updateProfileData(editedData); 
                setUserData(updatedData);
                setIsEditing(false);
                window.location.reload();
            } catch (error) {
                console.error('Error updating profile:', error);
            }
        } else {
            console.error('Edited data is null');
        }
    };


  if (!userData) return <div>Loading...</div>;

  if (isEditing) {
    return (
      <div>
        <h1>Edit Profile</h1>
        <input 
          name="nickname"
          value={editedData?.nickname ?? ''}
          onChange={handleInputChange}
          placeholder="Nickname"
        />
        <input 
          name="email"
          value={editedData?.email ?? ''}
          onChange={handleInputChange}
          placeholder="Email"
        />
        <input 
          name="self_name"
          value={editedData?.self_name ?? ''}
          onChange={handleInputChange}
          placeholder="Username"
        />
        <input 
          type="file"
          onChange={handleImageChange}
        />
        <input 
          name="first_name"
          value={editedData?.first_name ?? ''}
          onChange={handleInputChange}
          placeholder="First Name"
        />
        <input 
          name="last_name"
          value={editedData?.last_name ?? ''}
          onChange={handleInputChange}
          placeholder="Last Name"
        />
        <textarea 
          name="introduction"
          value={editedData?.introduction ?? ''}
          onChange={handleInputChange}
          placeholder="Introduction"
        />
        <textarea 
          name="interest"
          value={editedData?.interest ?? ''}
          onChange={handleInputChange ?? ''}
          placeholder="Interest"
        />
        <button onClick={handleEditSubmit}>Update Profile</button>
      </div>
    );
  }

  return (
    <div>
      <h1>{userData.nickname}</h1>
      <img src={userData.img || 'defaultImageURL'} alt={`${userData.nickname} 的頭像`} />
      <p>用戶名稱: {userData.username}</p>
      <p>電子郵件: {userData.email}</p>
      <p>姓名: {userData.first_name} {userData.last_name}</p>
      <p>自我介紹: {userData.introduction}</p>
      <p>興趣: {userData.interest}</p>
      {!user_id && <button onClick={() => setIsEditing(true)}>Edit</button>}
    </div>
  );
};

export default MyProfile;
